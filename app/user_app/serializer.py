from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from .models import User

class userSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = "__all__"
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "username",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user