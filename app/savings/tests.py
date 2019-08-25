import json
from account.models import User
from .models import GroupAccount, MemberAccount
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from datetime import date,timedelta,datetime

# class for creating User
class UserDetails:
    def createUser(self,username,full_name,email,password):
        return User.objects.create_user(username, email,password)
    
    def api_authentication(self,user,client):
        return client.credentials(HTTP_AUTHORIZATION='Token ' + user.token)

# class for creating a group
class CreateGroup:
        group_create_data = {
            "name":"cowry_diamond","amount":"570000","maximum_amount":"140000",
            "description":"This is a bronze account with minimum savings of 70000",
            "duration":1,"interval":"monthly"
            }

        @property
        def get_duration(self):
            interval = self.group_create_data.get('interval')
            duration = self.group_create_data.get('duration')
            set_interval = None
            if interval == 'weekly':
                set_interval = datetime.now() + timedelta(weeks=duration)
                self.group_create_data.update({"end_date":f"{set_interval}"})
            elif interval == 'monthly':
                set_interval = datetime.now() + timedelta(days=duration * 30)
                self.group_create_data.update({"end_date":f"{set_interval}"})
            else:
                set_interval = datetime.now() + timedelta(days=duration * 365.25)
                self.group_create_data.update({"end_date":f"{set_interval}"})
            return set_interval

        def create_group(self,user_id):
            group = GroupAccount.objects.create(
                name= self.group_create_data['name'],\
                amount = self.group_create_data['amount'],\
                maximum_amount = self.group_create_data['maximum_amount'],\
                description = self.group_create_data['description'],\
                end_date = self.get_duration ,\
                group_admin = user_id)

            return group





class UserUpdateToGroupAdminAPIViewTestCase(APITestCase):
    url = reverse("savings:is_group_admin")
    user_detail = UserDetails()
    def setUp(self):
        self.username = "temitayo"
        self.email = "temitayo@bakare.com"
        self.full_name ="Oluwaseun Somefun"
        self.is_group_admin = True
        self.password = "password"
        self.user = self.user_detail.createUser(self.username,self.email,self.full_name,\
                                                self.password)
        self.user_detail.api_authentication(self.user,self.client)



    def test_update_user(self):
        response = self.client.put(self.url,{"is_group_admin":self.is_group_admin,
                                    },format='json')        
        self.assertEqual(200, response.status_code)



class CreateUpdateGroupAccountAPIViewTestCase(APITestCase):
        user_detail = UserDetails()
        create_group_url = reverse("savings:create_group")
        create_group = CreateGroup()
        def setUp(self):
            self.username = "temitayo"
            self.email = "temitayo@bakare.com"
            self.full_name = "Oluwaseun Somefun"
            self.password = "password"

            self.user = self.user_detail.createUser(self.username,self.email,self.password,\
                                                    self.full_name)

            self.user_detail.api_authentication(self.user,self.client)

            self.group_admin = User.objects.filter(id=self.user.id).update(is_group_admin=True)
            self.user_id = User.objects.get(id=self.user.id)

            self.group_test_create_data = {
            "name":"cowry_silver","amount":"60000","maximum_amount":"120000",
            "description":"This is a bronze account with minimum savings of 60000",
            "duration":1,"interval":"monthly","group_admin":f"{self.user_id}"
            }

            
            self.group_update_data = {
            "name":"cowry_silver","amount":"60000","maximum_amount":"120000",
            "description":"This is a silve account with minimum savings of 60000",
            "duration":1,"interval":"monthly"
                }

    
        def test_create_group_account(self):
                
            response = self.client.post(self.create_group_url,self.group_test_create_data,\
                                        format='json')
            self.assertEqual(201, response.status_code)

            response = self.client.post(self.create_group_url,self.group_test_create_data,\
                                        format='json')
            self.assertEqual(400, response.status_code)

        def test_update_group_account(self):
            group = self.create_group.create_group(self.user_id)
            group = GroupAccount.objects.get(id=group.id)
            response = self.client.put(reverse('savings:update_group',kwargs={'id':group.id}),\
                                        self.group_update_data,format='json')
            self.assertEqual(200, response.status_code)



class CreateUpdateSavingsAccountAPIViewTestCase(APITestCase):
        user_detail = UserDetails()
        create_savings_url = reverse("savings:create_saving")
        create_group = CreateGroup()

        def setUp(self):
            self.username = "oseun"
            self.email = "justthinking@gmail.com"
            self.password = "password"
            self.full_name ="Oluwaseun Somefun"
            self.group_name = "cowry_diamond"
            self.user = self.user_detail.createUser(self.username,self.full_name,\
                                                    self.email,self.password)

            self.user_update = User.objects.filter(id=self.user.id).\
                                update(phone_number='07058877797',is_group_admin=True)

            self.user2 = self.user_detail.createUser("faith","oluwole faith",\
                                                    "faith@gmail.com","password")

            self.user_detail.api_authentication(self.user,self.client)


            self.user2_update = User.objects.filter(id=self.user2.id).\
                                update(phone_number='07058877787')

            self.user_id = User.objects.get(id=self.user.id)

            self.user_id2 = User.objects.get(id=self.user2.id)

            self.group = self.create_group.create_group(self.user)

            self.group = GroupAccount.objects.get(name=self.group_name)

            self.savings_create_data = {
                "group":f"{self.group}","amount":"80000","member":self.user_id,
                "member_name":"oluwole faith"
                }
                

            self.savings_test_create_data = {
                "group":f"{self.group}","amount":"60000","member":f"{self.user_id2}",
                "member_name":f"{self.user.full_name}"
                }

            self.savings_update_data = {"amount":"90000"}

    
        def test_create_savings_account(self):
            response = self.client.post(self.create_savings_url,self.savings_test_create_data,\
                                        format='json')

            self.assertEqual(201, response.status_code)

        def test_update_savings_account(self):
            savings = MemberAccount.objects.create(
                group= self.group,\
                amount = self.savings_create_data.get('amount'),\
                member = self.savings_create_data.get('member'),\
                member_name = self.savings_create_data.get('member_name'))
            savings = MemberAccount.objects.get(id=savings.id)
            response = self.client.put(reverse('savings:update_saving',kwargs={'id':savings.id}),\
                                        self.savings_update_data,format='json')
            self.assertEqual(200, response.status_code)