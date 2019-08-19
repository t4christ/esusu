from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.core import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import User


from .serializers import (RegistrationSerializer,LoginSerializer,UserSerializer)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    def post(self, request):
        password = request.data.get('password', {})
        confirm_password=request.data.get('confirm_password',{})
        if password == confirm_password:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return  Response({"message":"Passwords must match"})



class InviteRegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    def post(self,request,invite):
        password = request.data.get('password', {})
        confirm_password=request.data.get('confirm_password',{})
        if password == confirm_password:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            request.session[f"{request.data.get('username')}_invite"] = invite
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return  Response({"message":"Passwords must match"})



class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        
        if(request.user.is_superuser):
            if 'user' in cache:
                # get results from cache
                users = cache.get('user')
                return Response(users, status=status.HTTP_200_OK)
 
            else:
                users = User.objects.all()
                serialized_user = serializers.serialize('python', users)
                results = [user for user in serialized_user]
                # store data in cache
                cache.set("user",results, timeout=CACHE_TTL)
                return Response(results, status=status.HTTP_200_OK)

    def put(self, request):
        serializer_data = {
            'username': request.data.get('username', request.user.username),
            'full_name': request.data.get('full_name', request.user.full_name),
            'phone_number': request.data.get('phone_number', request.user.phone_number),
            'email': request.data.get('email', request.user.email),
        }
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        delete_user = get_object_or_404(User,username=request.user.username,pk=pk)
        delete_user.delete()
        return Response({"message":"Your account has been deleted."})

        



