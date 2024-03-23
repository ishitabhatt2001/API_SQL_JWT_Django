from django.urls import path
from .views import UpdateUser, UserCreateAPIView, UserDeleteAPIView, UserLoginAPIView, UserView, example_view

urlpatterns = [
    path('UsersView/', UserView.as_view(), name='user-view'),
    path('middleware/', example_view, name='middleware'),
    path('register/', UserCreateAPIView.as_view(), name='user-register'),#create user
    path('login/', UserLoginAPIView.as_view(), name='user-login'),#generate token
    path('UpdateUser/', UpdateUser.as_view(), name='user-update'),#update usser
    path('DeleteUser/', UserDeleteAPIView.as_view(), name='user-delete'),#if normal user
]