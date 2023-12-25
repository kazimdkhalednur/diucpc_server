from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from faker import Faker

from .models import Blog

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
        "status": fake.random_element(elements=("draft", "published")),
    }
    blog_2_data = {
        "title": fake.sentence(nb_words=6),
        "thumbnail": SimpleUploadedFile(
            name="images.jpg",
            content=open(image_path, "rb").read(),
            content_type="image/jpeg",
        ),
        "description": fake.paragraph(nb_sentences=5),
        "status": fake.random_element(elements=("draft", "published")),
    }

    def setUp(self):
        self.blog_1 = Blog.objects.create(**self.blog_1_data)
        self.blog_2 = Blog.objects.create(**self.blog_2_data)

    def test_blog_model(self):
        self.assertEqual(self.blog_1.title, self.blog_1_data["title"])
        self.assertEqual(self.blog_1.description, self.blog_1_data["description"])
        self.assertEqual(self.blog_1.status, self.blog_1_data["status"])
        if settings.DEBUG:
            self.assertEqual(
                self.blog_1.thumbnail.url,
                settings.MEDIA_URL + "blog/" + self.blog_1_data["thumbnail"].name,
            )

    def test_blog_model_count(self):
        self.assertEqual(Blog.objects.count(), 2)

    def test_blog_unique_slug(self):
        self.blog_slug_1 = Blog.objects.create(**self.blog_1_data)
        self.blog_slug_2 = Blog.objects.create(**self.blog_1_data)
        self.assertNotEqual(self.blog_slug_1.slug, self.blog_slug_2.slug)
        self.blog_slug_1.thumbnail.delete()
        self.blog_slug_2.thumbnail.delete()

    def test_blog_delete(self):
        self.blog_1.delete()
        self.assertEqual(Blog.objects.count(), 1)

    def test_blog_thumbnail_upload(self):
        if settings.DEBUG:
            self.assertEqual(
                self.blog_1.thumbnail.url,
                settings.MEDIA_URL + "blog/" + self.blog_1_data["thumbnail"].name,
            )
            self.assertEqual(
                self.blog_2.thumbnail.url,
                settings.MEDIA_URL + "blog/" + self.blog_2_data["thumbnail"].name,
            )

    def test_blog_delete_thumbnail(self):
        self.blog_1.delete()
        self.assertFalse(self.blog_1.thumbnail)

    def tearDown(self):
        self.blog_1.thumbnail.delete()
        self.blog_2.thumbnail.delete()
