from datetime import datetime
from io import BytesIO

import qrcode
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django_otp import devices_for_user, match_token
from django_otp.decorators import otp_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from users.models import User


class Change2faStatus(views.APIView):
    def post(self, request):
        user = request.user
        secret = request.data.get('secret')
        status = request.data.get('status')

        try:
            if status:
                token = verify_2fa_secret(user.email, secret)
            else:
                raise Exception(f"Cannot verify user with email={user.email}, secret={secret}")
            
            token = True  # TODO: TODO: TODO: TODO: TODO: TODO: TODO: 

            if token:    
                user.enable_google_2fa_verification = status
                user.save()
            else:
                raise Exception(f"Could not save the token in db. token={token}")

            return Response({
                "success": True,
            })
        except Exception as e:
            return Response({
                "success": False,
                "msg": str(e)
            })


class GetGoogleUrl(views.APIView):
    def get(self, request):
        return Response({'result': f'https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_OAUTH_CLIENT_ID}&redirect_uri={settings.GOOGLE_OAUTH_REDIRECT_URI}&scope=https://www.googleapis.com/auth/userinfo.email&response_type=code'})


class GenerateTOTPSecret(views.APIView):
    def get(self, request):
        # Get or create a TOTP device for the user
        user: User = request.user
        secret = self._get_user_2fa_secret(user)

        user.google_2fa_secret = secret
        user.save()

        google2fa_url = self._generate_qr_code_image(secret)

        return Response({
            'success': True,
            'secret': str(secret),
            'google2fa_url': str(google2fa_url)
        }, status=status.HTTP_201_CREATED)

    def _get_user_2fa_secret(self, user: User):
        # if user.enable_google_2fa_verification:
        #     return Response("google 2fa activated in the past", status=status.HTTP_400_BAD_REQUEST)

        devices = devices_for_user(user)
        device = next(
            (dev for dev in devices if isinstance(dev, TOTPDevice)), None)
        if not device:
            device = TOTPDevice.objects.create(
                user=user, name='My Device')

        secret = device.config_url
        user.google_2fa_secret = secret
        user.save()

        return secret

    def _generate_qr_code_image(self, secrete):
        qr = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(secrete)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Save the image file and return url
        filename = f"{slugify(datetime.now())}.jpg"
        default_storage.save(filename, ContentFile(buffer.read()))
        return default_storage.url(filename)


class ValidateTOTPToken(views.APIView):
    @method_decorator(otp_required)
    def post(self, request):
        code = request.data.get('code')
        email = request.data.get('email')
        sec_code = request.data.get('sec_code')
        token = verify_2fa_secret(email, code)

        if token:
            return Response(
                {
                    'success': True,
                    'access_Token': token
                }
            )

        return Response(
            {
                'success': False,
            }
        )

def verify_2fa_secret(email, code):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"Error:": f"Could not find user with email:{email}"}, status=status.HTTP_400_BAD_REQUEST)

    matched_devices = match_token(user, code)
    if matched_devices:
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    return False

class GoogleLogin(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        code = request.GET.get('code')
        # TODO: check this input data. It will receives this if referrer code is set in front:
        #       referrer_code
        #       recruited

        data = {
            'code': code,
            'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_OAUTH_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        token_response = requests.post(
            'https://oauth2.googleapis.com/token',
            data=data
        )
        if token_response.status_code != 200:
            return Response({'ERROR': token_response.content, 'data': data})

        token_data = token_response.json()

        id_token_data = id_token.verify_oauth2_token(
            token_data['id_token'], google_requests.Request(
            ), settings.GOOGLE_OAUTH_CLIENT_ID
        )

        try:
            user = User.objects.get(email=id_token_data['email'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user.enable_google_2fa_verification:
            return Response({
                '2fa': True,
                'security_code': user.google_2fa_secret,
                'user': {'email': id_token_data['email']}
            })

        else:
            token, _ = Token.objects.get_or_create(user=user)
            if not token.key:
                return Response("Token is empty!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({
                '2fa': False,
                'auth': {'access_token': token.key},
                'user': {'email': id_token_data['email']}
            })
