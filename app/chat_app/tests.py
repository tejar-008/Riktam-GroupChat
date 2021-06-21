import datetime
from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from chat_app.apps import ChatAppConfig
from django.urls import reverse
from .models import Group, GroupMessage
from user_app.models import User
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
        self.group1 = Group.objects.create(title="Group 1", created_by=self.user1)
        self.group2 = Group.objects.create(title="Group 2", created_by=self.user1)
        self.group3 = Group.objects.create(title="Group 3")
        self.group_message1 = GroupMessage.objects.create(message="Hi how are all?", group=self.group1, created_by=self.user1)
        # user1 login
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)


class TestChatApp(ObjectsCreation, TestCase):
    def test_app_file(self):
        self.assertEqual(ChatAppConfig.name, "chat_app")

    def test_groupCreate(self):
        # self.client.logout()
        response = self.client.post(reverse("chat_app:groupCreate"), data={
            "title": "Test Group 1",
            "is_private": True})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse("chat_app:groupCreate"), data={})
        self.assertEqual(response.status_code, 409)

    def test_groupList(self):
        # user1 login
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        # Group List GET with authentication
        response = self.client.get(
            reverse("chat_app:groupList"))
        self.assertEqual(response.status_code, 200)

    def test_groupDetail(self):
        # Group detail GET view with authentication
        # Valid group ID
        response = self.client.get(
            reverse(
                "chat_app:groupDetail", kwargs={'pk': self.group2.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        # InValid group ID
        response = self.client.get(
            reverse(
                "chat_app:groupDetail", kwargs={'pk': 55}
            )
        )
        self.assertEqual(response.status_code, 404)

        # Valid PUT method
        response = self.client.put(
            reverse(
                "chat_app:groupDetail", kwargs={'pk': self.group2.id}
            ), data={
                "title": "Group 2",
                "is_private": True,
            }
        )
        self.assertEqual(response.status_code, 204)
        # PUT to update created_by field
        response = self.client.put(
            reverse(
                "chat_app:groupDetail", kwargs={'pk': self.group3.id}
            ), data={
                "title": "Group 3",
                "is_private": True,
            }
        )
        self.assertEqual(response.status_code, 204)
        # InValid PUT method
        response = self.client.put(
            reverse(
                "chat_app:groupDetail", kwargs={'pk': self.group2.id}
            ), data={
                "username": "user2"
            }
        )
        self.assertEqual(response.status_code, 409)

        # Valid Group ID DELETE
        response = self.client.delete(
            reverse(
                "chat_app:groupDetail", kwargs={'pk': self.group2.id}
            )
        )
        self.assertEqual(response.status_code, 204)

    def test_groupMember(self):
        # GroupMember detail GET view with authentication
        # Valid group ID
        response = self.client.get(
            reverse(
                "chat_app:groupMember", kwargs={'pk': self.group1.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        # InValid group ID
        response = self.client.get(
            reverse(
                "chat_app:groupMember", kwargs={'pk': 44}
            )
        )
        self.assertEqual(response.status_code, 404)
        # GroupMember detail PUT view with authentication
        # Valid groupMember Add
        response = self.client.put(
            reverse(
                "chat_app:groupMember", kwargs={'pk': self.group1.id}
            ), data={"members": [self.user1.id, self.user2.id]}
        )
        self.assertEqual(response.status_code, 204)

        # InValid groupMember Add
        response = self.client.put(
            reverse(
                "chat_app:groupMember", kwargs={'pk': self.group1.id}
            ), data={"members": [self.user1.id, 22]}
        )
        self.assertEqual(response.status_code, 409)

    def test_groupChat(self):
        # groupChat detail GET view with authentication
        # Valid group ID
        response = self.client.get(
            reverse(
                "chat_app:groupChat", kwargs={'pk': self.group1.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        # Valid group ID with no messages
        response = self.client.get(
            reverse(
                "chat_app:groupChat", kwargs={'pk': self.group2.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        # InValid group ID
        response = self.client.get(
            reverse(
                "chat_app:groupChat", kwargs={'pk': 44}
            )
        )
        self.assertEqual(response.status_code, 404)
        # groupChat detail POST view with authentication
        # Valid group ID
        response = self.client.post(
            reverse(
                "chat_app:groupChat", kwargs={'pk': self.group1.id}
            ), data={"message": "Hi I am user1"}
        )
        self.assertEqual(response.status_code, 201)
        # InValid group ID
        response = self.client.post(
            reverse(
                "chat_app:groupChat", kwargs={'pk': self.group1.id}
            ), data={}
        )
        self.assertEqual(response.status_code, 409)

    def test_MessageLike(self):
        # MessageLike detail GET view with authentication
        # Valid group ID
        response = self.client.get(
            reverse(
                "chat_app:messageLike", kwargs={'group_id': self.group1.id, 'msg_id': self.group_message1.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        # Valid group ID with no messages
        response = self.client.get(
            reverse(
                "chat_app:messageLike", kwargs={'group_id': self.group1.id, 'msg_id': self.group_message1.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        # InValid group ID
        response = self.client.get(
            reverse(
                "chat_app:messageLike", kwargs={'group_id': 123, 'msg_id': self.group_message1.id}
            )
        )
        self.assertEqual(response.status_code, 404)
        # groupChat detail POST view with authentication
        # Message like
        response = self.client.post(
            reverse(
                "chat_app:messageLike", kwargs={'group_id': self.group1.id, 'msg_id': self.group_message1.id}
            )
        )
        self.assertEqual(response.status_code, 204)
        # Message Unlike
        response = self.client.post(
            reverse(
                "chat_app:messageLike", kwargs={'group_id': self.group1.id, 'msg_id': self.group_message1.id}
            )
        )
        self.assertEqual(response.status_code, 204)

