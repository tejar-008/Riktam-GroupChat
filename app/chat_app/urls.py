from django.urls import path
from .views import (GroupList, GroupDetail, GroupCreate, GroupMember, GroupChat, MessageLike)

app_name = "chat_app"

urlpatterns = [
    path('group/<int:pk>/member/', GroupMember.as_view(), name="groupMember"),
    path('group/<int:pk>/chat/', GroupChat.as_view(), name="groupChat"),
    path('group/<int:group_id>/message/<int:msg_id>/', MessageLike.as_view(), name="messageLike"),
    path('group-list/', GroupList.as_view(), name="groupList"),
    path('group-create/', GroupCreate.as_view(), name="groupCreate"),
    path('group/<int:pk>/', GroupDetail.as_view(), name="groupDetail"),
]