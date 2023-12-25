import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from faker import Faker

from ..models import User
from ..utils import profile_photo_path

fake = Faker()


class UserModelTestCase(TestCase):
    """Test for User Model"""

    image_path = settings.BASE_DIR / "test/pictures/images.png"
    user_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "username": fake.user_name(),
        "password": fake.password(),
        "role": fake.random_element(
            elements=(choices[0] for choices in User.USER_ROLE_CHOICES)
        ),
        "profile_photo": SimpleUploadedFile(
            name="images.png",
            content=open(image_path, "rb").read(),
            content_type="image/png",
        ),
    }

    def setUp(self):
        self.user = User.objects.create_user(**self.user_data)

    def test_user_model_str(self):
        self.assertEqual(str(self.user), self.user_data["email"])

    def test_create_user(self):
        temp_user_data = self.user_data.copy()
        temp_user_data.pop("profile_photo")

        self.assertTrue(self.user.check_password(temp_user_data.pop("password")))
        self.assertEqual(
            self.user.profile_photo.url,
            settings.MEDIA_URL
            + profile_photo_path(self.user, self.user_data["profile_photo"].name),
        )
        for key, value in temp_user_data.items():
            self.assertEqual(getattr(self.user, key), value)

    def test_user_count(self):
        self.assertEqual(User.objects.count(), 1)

    def test_user_delete(self):
        self.user.delete()
        self.assertEqual(User.objects.count(), 0)

    def test_user_default_role(self):
        user = User.objects.create_user(
            email=fake.email(),
            username=fake.name(),
            password=fake.password(),
        )
        self.assertEqual(user.role, "general")

    def test_user_profile_photo_update(self):
        image_path = settings.BASE_DIR / "test/pictures/images.jpg"
        old_image_path = self.user.profile_photo.path
        self.user.profile_photo = SimpleUploadedFile(
            name="images.jpg",
            content=open(image_path, "rb").read(),
            content_type="image/jpeg",
        )
        self.user.save()

        self.assertFalse(os.path.exists(old_image_path))
        self.assertNotEqual(old_image_path, self.user.profile_photo.path)
        self.assertTrue(
            self.user.profile_photo.url.endswith(self.user.profile_photo.name)
        )

    def tearDown(self):
        self.user.profile_photo.delete()
