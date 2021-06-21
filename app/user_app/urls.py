from django.urls import path, include
from .views import *

app_name = "user_app"

urlpatterns = [
    path('login/', UserLogin.as_view(), name="userLogin"),
    path('logout/', UserLogout.as_view(), name="userLogout"),
    path('user-list/', UserList.as_view(), name="userList"),
    path('user-create/', UserCreate.as_view(), name="userCreate"),
    path('user/<int:pk>/', UserDetail.as_view(), name="userDetail"),
]