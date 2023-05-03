from django.urls import reverse
from django.http import HttpRequest
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.utils import timezone

from apps.banner.models import Banner
from apps.banner.serializers.user_serializers import BannerListSerializer
from apps.users.models import User


class BannerListAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@gmail.com',
            name='John Doe',
        )
        self.token = Token.objects.create(
            user=self.user,
        )
        self.api_authentication_header = f'Token {self.token.key}'

        self.banner_published = Banner.objects.create(
            title='Published Banner',
            author='John Doe',
            image='banner/test_image.jpg',
            status=Banner.PUBLISH,
            summary='This is a published banner summary.',
            text='This is a published banner text.',
            publish_date=timezone.now(),
        )
        self.banner_draft = Banner.objects.create(
            title='Draft Banner',
            author='Jane Doe',
            image='banner/test_image.jpg',
            status=Banner.DRAFT,
            summary='This is a draft banner summary.',
            text='This is a draft banner text.',
            publish_date=timezone.now(),
        )

        self.url = reverse('banner_user:list')

    def test_banner_list_api_view_get(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )

        banners = Banner.objects.filter(
            status=Banner.PUBLISH,
        ).order_by('publish_date')

        # Create a fake HttpRequest object and update it with the necessary data
        request = HttpRequest()
        request.META['SERVER_NAME'] = 'testserver'
        request.META['SERVER_PORT'] = '80'
        request.META['HTTP_AUTHORIZATION'] = self.api_authentication_header

        serializer = BannerListSerializer(
            banners,
            many=True,
            context={"request": request},
        )

        expected_response = {
            "success": True,
            "code": 200,
            "data": serializer.data,
            "message": "Data retrieved successfully"
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_draft_banners_are_not_shown(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )

        for banner_data in response.data['data']:
            self.assertNotEqual(
                banner_data['title'],
                self.banner_draft.title,
            )
