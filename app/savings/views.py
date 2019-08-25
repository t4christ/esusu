from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.core import serializers
from rest_framework import status
from datetime import date,timedelta,datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from .models import MemberAccount, GroupAccount
from .serializers import GroupSerializer,MemberSerializer,GetGroupSerializer
from account.serializers import UserSerializer
from .generate_invite import InviteCode
from django.core import mail
from django.conf import settings



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class HomeAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self,request,format=None):
        return Response({"Message":"You are welcome to esusu"},status=status.HTTP_200_OK)




class SearchGroupAPIView(ListAPIView):
    # Allow only authenticated users to hit this endpoint.
    serializer_class = GetGroupSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        group_name = self.request.query_params.get('group_name', None)
        if group_name in cache:
                # get results from cache
                groups = cache.get(group_name)
                return groups
 
        else:
                queryset = GroupAccount.objects.filter(is_searchable=True)
                if group_name is not None:
                    filter_group = queryset.filter(name=group_name) 
                    # store data in cache
                    cache.set(group_name,filter_group, timeout=CACHE_TTL)
                    return filter_group 
                else:
                    return queryset







class GroupMemberListAPIView(APIView):
    # Allow only authenticated users to hit this endpoint.
    permission_classes = (IsAuthenticated,)
    
    def get(self, request,group_name):
        if(request.user.is_group_admin):
            if 'member_list' in cache:
                # get results from cache
                members = cache.get('member_list')
                return Response(members, status=status.HTTP_200_OK)
 
            else:
                group = GroupAccount.objects.get(name=group_name)
                member_list = MemberAccount.objects.select_related('group').all()
                serialized_member = serializers.serialize('python', member_list)
                results = [member for member in serialized_member]
                # store data in cache
                cache.set("member_list",results, timeout=CACHE_TTL)
                return Response(results, status=status.HTTP_200_OK)
        else:
            return Response({"message":"You must be a group admin to view members"})       




class GroupAdminAPIView(APIView):
    # Allow only authenticated users to hit this endpoint.
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def put(self, request):
        serializer_data = {
            'is_group_admin': request.data.get('is_group_admin',None)
        }
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateGroupAPIView(APIView):
    # Allow only authenticated users to hit this endpoint.
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        interval = request.data.get('interval')
        duration = int(request.data.get('duration'))
        set_interval = None
        if interval == 'weekly':
            set_interval = datetime.now() + timedelta(weeks=duration)
        elif interval == 'monthly':
            set_interval = datetime.now() + timedelta(days=duration * 30)
        else:
            set_interval = datetime.now() + timedelta(days=duration * 365.25)
            
        if request.user.is_group_admin:
            serializer.save(group_admin=request.user,end_date=set_interval)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"You must be a group admin to create a coperate account"})


class UpdateGroupAdminAPIView(APIView):
    # Allow only authenticated users to hit this endpoint.
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    def put(self, request,id):
        queryset = GroupAccount.objects.get(id=id)
        serializer_data = {
        'amount': request.data.get('amount'),
        'maximum_amount': request.data.get('maximum_amount'),
        'end_date':queryset.end_date,
        'description': request.data.get('description'),
        'name': request.data.get('name')}

        interval = request.data.get('interval')
        duration = int(request.data.get('duration'))
        set_interval = queryset.end_date
        if interval == 'weekly' and duration:
                set_interval = datetime.now() + timedelta(weeks=duration)
                
        elif interval == 'monthly' and duration:
            set_interval = datetime.now() + timedelta(days=duration * 30)
            
        elif interval == 'yearly' and duration:
            set_interval = datetime.now() + timedelta(days=duration * int(365.25))
        

        serializer = self.serializer_class(
            queryset, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(end_date=set_interval)
        return Response(serializer.data, status=status.HTTP_200_OK)




class CreateSavingAPIView(APIView):
    # Allow only authenticated users to hit this endpoint.
    permission_classes = (IsAuthenticated,)
    serializer_class = MemberSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            group = get_object_or_404(GroupAccount,name=request.data.get('group'))
            member = MemberAccount.objects.filter(member=request.user).count()
            if member > 0:
                return Response({"message":"You can only save ones in a period interval"})
            serializer.save(end_date=group.end_date,member=request.user,group=group,\
                            member_name=request.user.full_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message":"Group name does not exist"})



class InviteCreateSavingAPIView(APIView):
    # Allow only authenticated users to hit this endpoint.
    permission_classes = (IsAuthenticated,)
    serializer_class = MemberSerializer
    def post(self,request,invite):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        

        if request.session.get(f'{request.user.username}_invite') == invite:
                
                get_invite = request.session.get(f'{request.user.username}_invite')
                c = InviteCode()
                get_data = c.jwt_extract_handler(get_invite) 
                invite_date = get_data.get('expiry_date')
                expiry_date_obj = datetime.strptime(invite_date,'"%Y-%m-%dT%H:%M:%S.%f"')
                utc_now = datetime.utcnow() 
                if expiry_date_obj < utc_now - timedelta(minutes=10):
                    return Response({"message":"Invitation token has expired"})
                try:
                    group = get_object_or_404(GroupAccount,name=get_data.get('group_name'))
                    member = MemberAccount.objects.filter(member=request.user).count()
                    if member > 0:
                        return Response({"message":"You can only save ones in a period interval"})
                except Exception as e:
                    return Response({"message":f"Group does not exist"})
                serializer.save(end_date=group.end_date,member=request.user,group=group,\
                            member_name=request.user.full_name)
                request.session.pop(f'{request.user.username}_invite')
        return Response(serializer.data, status=status.HTTP_200_OK)









class UpdateSavingAPIView(APIView):
    # Allow only authenticated users to hit this endpoint.
    permission_classes = (IsAuthenticated,)
    serializer_class = MemberSerializer
    def put(self, request, id):
        queryset = MemberAccount.objects.get(id=id)
        serializer_data = {'amount': request.data.get('amount',queryset.amount)}
        serializer = self.serializer_class(
            queryset, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendInviteAPIView(APIView):
    # Allow only authenticated users to hit this endpoint.
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if request.user.is_group_admin:
            try:
                name = request.data.get('name')
                email = request.data.get('email')
                group_name = GroupAccount.objects.get(name=name)
                code = InviteCode(request)
                get_invite = code.invite_code(group_name.name)
                link = f"http://esusudocker-env.nb2m2kzsxk.us-east-2.elasticbeanstalk.com\
                        /api/v1/register/{get_invite}"
                message = f"{request.user.full_name} has invited you to join {group_name.name}\
                             co-operate savings"
                mail.send_mail('Cowrywise Invite',f'{message} via link {link}{get_invite}',\
                                settings.EMAIL_HOST_USER,[email])
                return Response({"message":"Invite sent"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message":f"{e}"})
        else:
            return Response({"message":"You must be a group admin to send an invite"})



        



