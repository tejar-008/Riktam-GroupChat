from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from .models import Group, GroupMessage
from user_app.serializer import userSerializer


class groupSerializer(serializers.ModelSerializer):
    members = userSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        # fields = "__all__"
        fields = [
            "id",
            "title",
            "is_private",
            "members",
            "created_by",
            "created_on",
        ]


class groupCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        # fields = "__all__"
        fields = [
            # "id",
            "title",
            "is_private",
            "members",
            # "created_on",
        ]
        extra_kwargs = {'members': {'required': False}}

    def create(self, validated_data):
        group = super(groupCreateSerializer, self).create(validated_data)
        group.save()
        return group


class groupAddMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        # fields = "__all__"
        fields = [
            "members"
        ]
        extra_kwargs = {'members': {'required': False}}


class groupMessageSerializer(serializers.ModelSerializer):
    is_liked_by = userSerializer(read_only=True, many=True)
    # group = groupSerializer(read_only=True)
    created_by = userSerializer(read_only=True)

    class Meta:
        model = GroupMessage
        # fields = "__all__"
        fields = [
            "id",
            "message",
            "is_liked_by",
            "group",
            "created_by",
            "created_on",
        ]


class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMessage
        # fields = "__all__"
        fields = [
            # "id",
            "message",
            # "group",
        ]
        extra_kwargs = {'group': {'required': False},
        }

# class messageLikeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Group
#         # fields = "__all__"
#         fields = [
#             "is_liked_by"
#         ]
#         extra_kwargs = {'is_liked_by': {'required': False}}
