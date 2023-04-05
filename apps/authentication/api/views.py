from django.shortcuts import redirect
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from utils.authentication import create_google_url, callback_google

from apps.users.models import User


class GoogleLogin(views.APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        url = create_google_url()
        return Response({'url': url})


class GoogleCallback(views.APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        id_info = callback_google(request)

        user_email = id_info['email']
        user_name = id_info['name']

        user = User.objects.get(email=user_email)
        token, created = Token.objects.get_or_create(user=user)

        redirect_url = "http://localhost:8080/dashboard/?token={0}&email={1}".format(
            token,
            user_email,
        )

        return redirect(redirect_url)


class Logout(views.APIView):
    def get(self, request):
        try:
            Token.objects.get(user=request.user).delete()
        except User.DoesNotExist:
            return Response({"Error:": f"Could not find user with email:{request.user.email}"}, status=status.HTTP_400_BAD_REQUEST)
