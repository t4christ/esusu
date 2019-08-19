import json
from account.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserRegistrationAPIViewTestCase(APITestCase):
    url = reverse("account:register_user")

    def test_user_registeration(self):
        """
        Test to register a valid user
        """
        user_data = {
            "username": "testuser",
            "full_name":"Temitayo Bakare",
            "email": "test@testuser.com",
            "phone_number":"0706888453",
            "password": "password",
            "confirm_password": "password",
        }
        response = self.client.post(self.url, user_data,format='json')
        self.assertEqual(201, response.status_code)

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "username": "testuser",
            "full_name":"Temitayo Bakare",
            "email": "test@testuser.com",
            "phone_number":"0706888453",
            "password": "password",
            "confirm_password": "password",
        }
        response = self.client.post(self.url, user_data_1,format='json')
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "username": "testuser",
            "full_name":"Temitayo Bakare",
            "email": "test@testuser.com",
            "phone_number":"0706888453",
            "password": "password",
            "confirm_password": "password",

        }
        response = self.client.post(self.url, user_data_2,format='json')
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("account:login")

    def setUp(self):
        self.username = "temitayo"
        self.email = "temitayo@bakare.com"
        self.password = "password"
        

        self.user = User.objects.create_user(self.username, self.email,self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "temitayo"},format='json')
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):

        response = self.client.post(self.url, {"username": self.username, "password": "paword"},format='json')
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):

        response = self.client.post(self.url,{"username": self.username, "password": self.password},format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))


class UserUpdateDeleteAPIViewTestCase(APITestCase):
    # def url(self, key):
    url = reverse("account:update_user")

    def setUp(self):
        self.username = "temitayo"
        self.email = "temitayo@bakare.com"
        self.full_name ="Temitayo Bakare"
        self.phone_number='0809777654'
        self.password = "password"
        self.confirm_password ="password"
        self.user = User.objects.create_user(self.username, self.email,self.password)
        self.api_authentication()

    def api_authentication(self):
           self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
     
    
    def test_update_user(self):
    
        response = self.client.put(self.url,{"full_name":self.full_name,
                                    "phone_number":self.phone_number,
                                    },format='json')
        response_data = json.loads(response.content)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(200, response.status_code)


    def test_delete_user(self):
            
            response = self.client.delete(reverse("account:delete_user",
                        kwargs={"pk": self.user.pk}))
            self.assertEqual(200, response.status_code)