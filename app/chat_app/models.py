import os
from django.db import models
from user_app.models import User


class Group(models.Model):
    title = models.CharField(max_length=100, unique=True)
    is_private = models.BooleanField(default=False)
    members = models.ManyToManyField(User, blank=True, related_name='group_members')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GroupMessage(models.Model):
    message = models.CharField(max_length=1000)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_liked_by = models.ManyToManyField(User, blank=True, related_name='group_message')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
