from django.utils.decorators import method_decorator
from django_otp import devices_for_user, match_token
from django_otp.decorators import otp_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status
from rest_framework.response import Response
from rest_framework import views


class GenerateTOTPSecret(views.APIView):
    def post(self, request):
        # Get or create a TOTP device for the user
        devices = devices_for_user(request.user)
        device = next(
            (dev for dev in devices if isinstance(dev, TOTPDevice)), None)
        if not device:
            device = TOTPDevice.objects.create(
                user=request.user, name='My Device')

        # Return the TOTP URI to the frontend
        return Response({'totp_uri': device.config_url}, status=status.HTTP_201_CREATED)


class ValidateTOTPToken(views.APIView):
    @method_decorator(otp_required)
    def post(self, request):
        token = request.data.get('totp_token')
        matched_devices = match_token(request.user, token)
        return Response({'is_valid': bool(matched_devices)}, status=status.HTTP_200_OK)

