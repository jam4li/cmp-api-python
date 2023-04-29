from django.urls import reverse
from django.http import HttpRequest
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.utils import timezone

from apps.announcement.models import Announcement
from apps.announcement.serializers.user_serializers import AnnouncementListSerializer
from apps.users.models import User


class AnnouncementListAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@gmail.com',
            name='John Doe',
        )
        self.token = Token.objects.create(
            user=self.user,
        )
        self.api_authentication_header = f'Token {self.token.key}'

        self.announcement_published = Announcement.objects.create(
            title='Published Announcement',
            author='John Doe',
            image='announcement/test_image.jpg',
            status=Announcement.PUBLISH,
            summary='This is a published announcement summary.',
            text='This is a published announcement text.',
            publish_date=timezone.now(),
        )
        self.announcement_draft = Announcement.objects.create(
            title='Draft Announcement',
            author='Jane Doe',
            image='announcement/test_image.jpg',
            status=Announcement.DRAFT,
            summary='This is a draft announcement summary.',
            text='This is a draft announcement text.',
            publish_date=timezone.now(),
        )

        self.url = reverse('announcement_user:list')

    def test_announcement_list_api_view_get(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )

        announcements = Announcement.objects.filter(
            status=Announcement.PUBLISH,
        ).order_by('publish_date')

        # Create a fake HttpRequest object and update it with the necessary data
        request = HttpRequest()
        request.META['SERVER_NAME'] = 'testserver'
        request.META['SERVER_PORT'] = '80'
        request.META['HTTP_AUTHORIZATION'] = self.api_authentication_header

        serializer = AnnouncementListSerializer(
            announcements,
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

    def test_draft_announcements_are_not_shown(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )

        for announcement_data in response.data['data']:
            self.assertNotEqual(
                announcement_data['title'],
                self.announcement_draft.title,
            )
