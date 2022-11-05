from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User

class LoginAPI(APIView):
    def post(self, request, **kwargs):
        data = request.data
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            return Response("Invalid username or password", status=status.HTTP_403_FORBIDDEN)
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class LogoutAPI(APIView):
    def post(self, request, **kwargs):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class RegisterAPI(APIView):
    def post(self, request, **kwargs):
        data = request.data
        if User.objects.filter(username=data["username"]).exists():
            return Response("Username already exists", status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(nickname=data["nickname"]).exists():
            return Response("Username already exists", status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(username=data["username"], nickname=data["nickname"])
        user.set_password(data["password"])
        user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CheckUsernameAPI(APIView):
    def get(self, request, **kwargs):
        pass
