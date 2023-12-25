from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from ..models import Blog

fake = Faker()


class BlogListAPIViewTestCase(APITestCase):
    """Test for Blog List API View"""

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

    blog_list_url = reverse("blogs:list")

    def setUp(self):
        self.blog_1 = Blog.objects.create(**self.blog_1_data)
        self.blog_2 = Blog.objects.create(**self.blog_2_data)
        self.blog_3 = Blog.objects.create(**self.blog_3_data)

    def test_blog_list_api_view(self):
        response = self.client.get(self.blog_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], self.blog_3_data["title"])
        self.assertEqual(response.data[1]["title"], self.blog_2_data["title"])

    def test_blog_delete_thumbnail(self):
        self.blog_1.delete()
        self.assertFalse(self.blog_1.thumbnail)

    def tearDown(self):
        self.blog_1.thumbnail.delete()
        self.blog_2.thumbnail.delete()
        self.blog_3.thumbnail.delete()
