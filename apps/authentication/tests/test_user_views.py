from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from apps.users.models import User


class GoogleAuthTest(APITestCase):
    def setUp(self):
        self.google_login_url = reverse('authentication_user:google-url')
        self.google_callback_url = reverse('authentication_user:callback')

        # TODO: Add logout
        # self.logout_url = reverse('logout')

        self.user = User.objects.create(
            email='test@gmail.com',
            name='John Doe',
        )
        self.token = Token.objects.create(
            user=self.user,
        )
        self.api_authentication_header = f'Token {self.token.key}'

    def test_google_login_url(self):
        response = self.client.get(self.google_login_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('url', response.data)

    def test_google_callback(self):
        # This test is challenging to implement because it depends on the Google API response.
        # You might consider mocking the Google API response using a library like 'responses'
        # or using a tool like 'vcrpy' to record and replay the API response.
        pass

    def test_logout(self):
        # TODO: Add test_logout
        pass
    #     response = self.client.get(
    #         self.logout_url,
    #         HTTP_AUTHORIZATION=self.api_authentication_header,
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     with self.assertRaises(Token.DoesNotExist):
    #         Token.objects.get(user=self.user)
