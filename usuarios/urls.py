from django.urls import path
from .views import login_view, logout_view, user_list, register_user

urlpatterns = [
    path('', user_list, name='user_list'),
    path('register/', register_user, name='register_user'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
