
from django.test import TestCase
from django.utils import timezone

from apps.announcement.models import Announcement


class AnnouncementModelTest(TestCase):
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

    def test_create_announcement(self):
        self.assertIsInstance(
            self.announcement,
            Announcement,
        )
        self.assertEqual(
            self.announcement.title,
            'Test Announcement',
        )
        self.assertEqual(
            self.announcement.author, 'John Doe')
        self.assertEqual(
            self.announcement.image,
            'announcement/test_img.jpg',
        )
        self.assertEqual(
            self.announcement.status,
            Announcement.PUBLISH,
        )
        self.assertEqual(
            self.announcement.summary,
            'This is a test summary.',
        )
        self.assertEqual(
            self.announcement.text,
            'This is a test text.',
        )

    def test_str_representation(self):
        self.assertEqual(str(self.announcement), 'Test Announcement')

    def test_update_announcement(self):
        self.announcement.title = 'Updated Test Announcement'
        self.announcement.author = 'Jane Doe'
        self.announcement.status = Announcement.DRAFT
        self.announcement.summary = 'This is an updated test summary.'
        self.announcement.text = 'This is an updated test text.'
        self.announcement.save()

        self.assertEqual(
            self.announcement.title,
            'Updated Test Announcement',
        )
        self.assertEqual(
            self.announcement.author,
            'Jane Doe',
        )
        self.assertEqual(
            self.announcement.status,
            Announcement.DRAFT,
        )
        self.assertEqual(
            self.announcement.summary,
            'This is an updated test summary.',
        )
        self.assertEqual(
            self.announcement.text,
            'This is an updated test text.',
        )

    def test_publish_date_set(self):
        self.assertIsNotNone(self.announcement.publish_date)
