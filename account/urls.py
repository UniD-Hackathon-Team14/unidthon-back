from django.urls import path

from .views import LoginAPI, LogoutAPI, RegisterAPI, CheckUsernameAPI

urlpatterns = [
    path("login/", LoginAPI.as_view(), name="login_api"),
    path("logout/", LogoutAPI.as_view(), name="logout_api"),
    path("register/", RegisterAPI.as_view(), name="register_api"),
    path("check_username", CheckUsernameAPI.as_view(), name="check_username_api")
]
