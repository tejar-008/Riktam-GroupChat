import datetime
from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from user_app.apps import UserAppConfig
from django.urls import reverse
from .models import User
from rest_framework.test import APIClient


class ObjectsCreation(object):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(
            first_name="user",
            last_name="1",
            username="user1",
            email="user1@gmail.com",
            is_superuser=True,
            is_staff=True,
        )
        self.user1.set_password("password")
        self.user1.save()
        self.token1 = Token.objects.get(user=self.user1)
        self.user2 = User.objects.create(
            first_name="user",
            last_name="2",
            username="user2",
            email="user2@gmail.com",
            is_superuser=False,
        )
        self.user2.set_password("password")
        self.user2.save()
        self.token2 = Token.objects.get(user=self.user2)
        # self.client.login(username="admin", password="password")
        # user1 login
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)


class TestUserApp(ObjectsCreation, TestCase):
    def test_app_file(self):
        self.assertEqual(UserAppConfig.name, "user_app")

    def test_userLogin(self):
        self.client.logout()
        response = self.client.post(reverse("user_app:userLogin"), data={"username": "user1", "password": "password"})
        self.assertEqual(response.status_code, 200)

    def test_userCreate(self):
        # self.client.logout()
        response = self.client.post(reverse("user_app:userCreate"), data={
            "username": "John",
            "email": "johndoe@gmail.com",
            "first_name": "John",
            "is_active": True,
            "last_name": "Doe",
            "password": "password"})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse("user_app:userCreate"), data={
            "username": "John"})
        self.assertEqual(response.status_code, 409)

    def test_userList(self):
        # user1 login
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        # User List GET with authentication
        response = self.client.get(
            reverse("user_app:userList"))
        self.assertEqual(response.status_code, 200)

    def test_userDetail(self):
        # User detail GET view with authentication
        # Valid user ID
        response = self.client.get(
            reverse(
                "user_app:userDetail", kwargs={'pk': self.user2.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        # Valid user ID
        response = self.client.get(
            reverse(
                "user_app:userDetail", kwargs={'pk': 55}
            )
        )
        self.assertEqual(response.status_code, 404)

        # Valid PUT method
        response = self.client.put(
            reverse(
                "user_app:userDetail", kwargs={'pk': self.user2.id}
            ), data={
                "username": "user2",
                "email": "user2@gmail.com",
                "first_name": "userr",
                "is_active": True,
                "last_name": "22",
                "password": "password"
            }
        )
        self.assertEqual(response.status_code, 204)
        # InValid PUT method
        response = self.client.put(
            reverse(
                "user_app:userDetail", kwargs={'pk': self.user2.id}
            ), data={
                "username": "user2"
            }
        )
        self.assertEqual(response.status_code, 409)

        # Valid user ID DELETE
        response = self.client.delete(
            reverse(
                "user_app:userDetail", kwargs={'pk': self.user2.id}
            )
        )
        self.assertEqual(response.status_code, 204)

    def test_userLogout(self):
        response = self.client.get(reverse("user_app:userLogout"))
        self.assertEqual(response.status_code, 200)
