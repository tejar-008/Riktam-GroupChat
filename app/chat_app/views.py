# from django.shortcuts import render
# from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from user_app.models import User
from .models import Group, GroupMessage
from .serializer import (
    groupSerializer,
    groupCreateSerializer,
    groupAddMemberSerializer,
    # messageLikeSerializer,
    groupMessageSerializer, MessageCreateSerializer
)


class GroupList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        groups = Group.objects.all()
        serializer = groupSerializer(groups, many=True)
        return Response(serializer.data)


class GroupCreate(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = groupCreateSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.created_by = request.user
            obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class GroupDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Group.objects.get(id=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        serializer = groupSerializer(group_obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        print(group_obj)
        serializer = groupCreateSerializer(instance=group_obj, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            if not obj.created_by:
                obj.created_by = request.user
                obj.save()
            return Response({
                "success": "Group Details Updated", "data": serializer.data
            },
                status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

    def delete(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        group_obj.delete()
        return Response({"success": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class GroupMember(APIView):
    def get_object(self, pk):
        try:
            return Group.objects.get(id=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        serializer = groupSerializer(group_obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        serializer = groupAddMemberSerializer(instance=group_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": "Users added/removed successfully",
                "data": serializer.data},
                status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class GroupChat(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Group.objects.get(id=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        group_messages = GroupMessage.objects.filter(group=group_obj).order_by("id")
        if group_messages:
            group_messages = groupMessageSerializer(group_messages, many=True)
            return Response(group_messages.data)  # serializer.data,
        return Response({"Message": "No Conversation"})

    def post(self, request, pk, format=None):
        group_obj = self.get_object(pk)
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_id=request.user.id, group_id=group_obj.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class MessageLike(APIView):
    def get_object(self, group_id, msg_id):
        try:
            return GroupMessage.objects.get(group_id=group_id, id=msg_id)
        except GroupMessage.DoesNotExist:
            raise Http404

    def get(self, request, group_id, msg_id, format=None):
        message_obj = self.get_object(group_id, msg_id)
        print(message_obj)
        serializer = groupMessageSerializer(message_obj)
        return Response(serializer.data)

    def post(self, request, group_id, msg_id, format=None):
        message_obj = self.get_object(group_id, msg_id)
        if request.user in message_obj.is_liked_by.all():
            message_obj.is_liked_by.remove(request.user.id)
            return Response({
                "success": "Unliked successfully"},
                status=status.HTTP_204_NO_CONTENT)
        else:
            message_obj.is_liked_by.add(request.user.id)
            return Response({
                "success": "Liked successfully"},
                status=status.HTTP_204_NO_CONTENT)
