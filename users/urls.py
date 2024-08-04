from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name="Home_page"),
    path("login_user", views.login_user, name="login user"),
    path("", views.login, name="Login_Page"),
    path("register", views.register, name="user_register"),
]
