from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_otp import devices_for_user
from django_otp.decorators import otp_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status
from rest_framework.response import Response
from rest_framework import views
from rest_framework.permissions import AllowAny


class TotpTemplateView(views.View):
    def get(self, request, pk=None, *args, **kwargs):
        return render(request, 'totp.html', {})


class GenerateTOTPSecret(views.APIView):
    def post(self, request):
        # Get or create a TOTP device for the user
        devices = devices_for_user(request.user)
        device = next(
            (dev for dev in devices if isinstance(dev, TOTPDevice)), None)
        if not device:
            device = TOTPDevice.objects.create(
                user=request.user, name='My Device')

        print(device.config_url)

        # Return the TOTP URI to the frontend
        return Response({'totp_uri': device.config_url}, status=status.HTTP_201_CREATED)


class ValidateTOTPToken(views.APIView):
    @method_decorator(otp_required)
    def post(self, request):
        # Get the TOTP device for the current user
        devices = devices_for_user(request.user)
        totp_device = next(
            (dev for dev in devices if isinstance(dev, TOTPDevice)), None)

        # Validate the submitted TOTP token
        is_valid = False
        if totp_device:
            token = request.data.get('totp_token')
            is_valid = totp_device.verify(token)

        # Return a JSON response indicating whether the token is valid or not
        return Response({'is_valid': is_valid}, status=status.HTTP_200_OK)
