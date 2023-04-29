from django.test import TestCase
from django.utils import timezone

from apps.announcement.models import Announcement
from apps.announcement.serializers.user_serializers import AnnouncementListSerializer


class AnnouncementListSerializerTest(TestCase):
    def setUp(self):
        self.announcement = Announcement.objects.create(
            title='Test Announcement',
            author='John Doe',
            image='announcement/test_img.jpg',
            status=Announcement.PUBLISH,
            summary='This is a test summary.',
            text='This is a test text.',
            publish_date=timezone.now(),
        )
        self.serializer = AnnouncementListSerializer(
            instance=self.announcement,
        )

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), [
            'title',
            'author',
            'image',
            'summary',
            'text',
            'publish_date',
        ])

    def test_correct_data(self):
        data = self.serializer.data
        self.assertEqual(
            data['title'],
            self.announcement.title,
        )
        self.assertEqual(
            data['author'],
            self.announcement.author,
        )
        self.assertEqual(
            data['image'],
            self.announcement.image.url,
        )
        self.assertEqual(
            data['summary'],
            self.announcement.summary,
        )
        self.assertEqual(
            data['text'],
            self.announcement.text,
        )
        # TODO: Write test for dates
