
from django.test import TestCase
from django.utils import timezone

from apps.banner.models import Banner


class BannerModelTest(TestCase):
    def setUp(self):
        self.banner = Banner.objects.create(
            title='Test Banner',
            author='John Doe',
            image='banner/test_img.jpg',
            status=Banner.PUBLISH,
            summary='This is a test summary.',
            text='This is a test text.',
            publish_date=timezone.now(),
        )

    def test_create_banner(self):
        self.assertIsInstance(
            self.banner,
            Banner,
        )
        self.assertEqual(
            self.banner.title,
            'Test Banner',
        )
        self.assertEqual(
            self.banner.author,
            'John Doe',
        )
        self.assertEqual(
            self.banner.image,
            'banner/test_img.jpg',
        )
        self.assertEqual(
            self.banner.status,
            Banner.PUBLISH,
        )
        self.assertEqual(
            self.banner.summary,
            'This is a test summary.',
        )
        self.assertEqual(
            self.banner.text,
            'This is a test text.',
        )

    def test_str_representation(self):
        self.assertEqual(str(self.banner), 'Test Banner')

    def test_update_banner(self):
        self.banner.title = 'Updated Test Banner'
        self.banner.author = 'Jane Doe'
        self.banner.status = Banner.DRAFT
        self.banner.summary = 'This is an updated test summary.'
        self.banner.text = 'This is an updated test text.'
        self.banner.save()

        self.assertEqual(
            self.banner.title,
            'Updated Test Banner',
        )
        self.assertEqual(
            self.banner.author,
            'Jane Doe',
        )
        self.assertEqual(
            self.banner.status,
            banner.DRAFT,
        )
        self.assertEqual(
            self.banner.summary,
            'This is an updated test summary.',
        )
        self.assertEqual(
            self.banner.text,
            'This is an updated test text.',
        )

    def test_publish_date_set(self):
        self.assertIsNotNone(self.banner.publish_date)
