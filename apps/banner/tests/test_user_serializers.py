from django.test import TestCase
from django.utils import timezone

from apps.banner.models import Banner
from apps.banner.serializers.user_serializers import BannerListSerializer


class BannerListSerializerTest(TestCase):
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
        self.serializer = BannerListSerializer(
            instance=self.banner,
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
            self.banner.title,
        )
        self.assertEqual(
            data['author'],
            self.banner.author,
        )
        self.assertEqual(
            data['image'],
            self.banner.image.url,
        )
        self.assertEqual(
            data['summary'],
            self.banner.summary,
        )
        self.assertEqual(
            data['text'],
            self.banner.text,
        )
        # TODO: Write test for dates
