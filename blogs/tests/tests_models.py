import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from faker import Faker

from ..models import Blog

fake = Faker()


class BlogModelTestCase(TestCase):
    """Test for Blog Model"""

    image_path = settings.BASE_DIR / "test/pictures/images.png"
    blog_1_data = {
        "title": fake.sentence(nb_words=6),
        "thumbnail": SimpleUploadedFile(
            name="images.png",
            content=open(image_path, "rb").read(),
            content_type="image/png",
        ),
        "description": fake.paragraph(nb_sentences=5),
        "status": Blog.BLOG_STATUS_CHOICES[0][0],
    }
    blog_2_data = {
        "title": fake.sentence(nb_words=6),
        "thumbnail": SimpleUploadedFile(
            name="images.jpg",
            content=open(image_path, "rb").read(),
            content_type="image/jpeg",
        ),
        "description": fake.paragraph(nb_sentences=5),
        "status": Blog.BLOG_STATUS_CHOICES[1][0],
    }
    blog_3_data = {
        "title": fake.sentence(nb_words=6),
        "thumbnail": SimpleUploadedFile(
            name="images.jpg",
            content=open(image_path, "rb").read(),
            content_type="image/jpeg",
        ),
        "description": fake.paragraph(nb_sentences=5),
        "status": Blog.BLOG_STATUS_CHOICES[1][0],
    }

    def setUp(self):
        self.blog_1 = Blog.objects.create(**self.blog_1_data)
        self.blog_2 = Blog.objects.create(**self.blog_2_data)
        self.blog_3 = Blog.objects.create(**self.blog_3_data)

    def test_blog_str(self):
        self.assertEqual(str(self.blog_1), self.blog_1.title)

    def test_blog_model(self):
        self.assertEqual(self.blog_1.title, self.blog_1_data["title"])
        self.assertEqual(self.blog_1.description, self.blog_1_data["description"])
        self.assertEqual(self.blog_1.status, self.blog_1_data["status"])
        self.assertTrue(
            self.blog_1.thumbnail.url.endswith(self.blog_1_data["thumbnail"].name)
        )

    def test_blog_model_count(self):
        self.assertEqual(Blog.objects.count(), 3)

    def test_blog_model_ordering(self):
        self.assertEqual(Blog.objects.first(), self.blog_3)
        self.assertEqual(Blog.objects.last(), self.blog_1)

    def test_blog_model_published_objects(self):
        self.assertEqual(Blog.published_objects.count(), 2)

    def test_blog_model_published_objects_ordering(self):
        self.assertEqual(Blog.published_objects.first(), self.blog_3)
        self.assertEqual(Blog.published_objects.last(), self.blog_2)

    def test_blog_unique_slug_with_same_title(self):
        self.blog_slug_1 = Blog.objects.create(**self.blog_1_data)
        self.blog_slug_2 = Blog.objects.create(**self.blog_1_data)
        self.assertNotEqual(self.blog_slug_1.slug, self.blog_slug_2.slug)
        self.blog_slug_1.thumbnail.delete()
        self.blog_slug_2.thumbnail.delete()

    def test_blog_update_thumbnail(self):
        image_path = settings.BASE_DIR / "test/pictures/images.jpg"
        old_thumbnail_path = settings.BASE_DIR / self.blog_1.thumbnail.path
        self.blog_1.thumbnail = SimpleUploadedFile(
            name="update_images.jpg",
            content=open(image_path, "rb").read(),
            content_type="image/jpeg",
        )
        self.blog_1.save()

        self.assertFalse(os.path.exists(old_thumbnail_path))
        self.assertNotEqual(old_thumbnail_path, self.blog_1.thumbnail.path)
        self.assertTrue(self.blog_1.thumbnail.url.endswith(self.blog_1.thumbnail.name))

    def test_blog_update_null_thumbnail(self):
        old_thumbnail_path = settings.BASE_DIR / self.blog_1.thumbnail.path
        self.blog_1.thumbnail = None
        self.blog_1.save()

        self.assertFalse(os.path.exists(old_thumbnail_path))
        self.assertFalse(self.blog_1.thumbnail)

    def test_blog_delete(self):
        self.blog_1.delete()
        self.assertEqual(Blog.objects.count(), 2)

    def test_blog_delete_thumbnail(self):
        self.blog_1.delete()
        self.assertFalse(self.blog_1.thumbnail)

    def tearDown(self):
        self.blog_1.thumbnail.delete()
        self.blog_2.thumbnail.delete()
        self.blog_3.thumbnail.delete()
