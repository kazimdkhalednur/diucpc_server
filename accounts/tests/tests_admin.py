from django.contrib.auth.models import Group
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker

from ..admin import CustomGroupAdmin, CustomUserAdmin
from ..models import User

fake = Faker()


class AdminCustomizationTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username=fake.user_name(), password=fake.password(), email=fake.email()
        )

        self.client = Client()
        self.client.force_login(self.admin_user)

    def test_custom_group_admin_permissions(self):
        group_add_url = reverse("admin:auth_group_add")
        request = self.client.get(group_add_url)
        request.user = self.admin_user
        admin = CustomGroupAdmin(Group, None)

        self.assertEqual(request.status_code, 200)
        self.assertTrue(admin.has_view_permission(request))
        self.assertTrue(admin.has_add_permission(request))
        self.assertTrue(admin.has_change_permission(request))
        self.assertTrue(admin.has_delete_permission(request))

    def test_custom_user_admin_permissions(self):
        user_add_url = reverse("admin:accounts_user_add")
        request = self.client.get(user_add_url)
        request.user = self.admin_user
        admin = CustomUserAdmin(User, None)

        self.assertEqual(request.status_code, 200)
        self.assertTrue(admin.has_view_permission(request))
        self.assertTrue(admin.has_add_permission(request))
        self.assertTrue(admin.has_change_permission(request))
        self.assertTrue(admin.has_delete_permission(request))

    def test_custom_user_admin_non_superuser_permissions(self):
        non_admin_user = User.objects.create_user(
            username=fake.user_name(), password=fake.password(), email=fake.email()
        )

        self.client.force_login(non_admin_user)

        user_change_url = reverse("admin:accounts_user_add")
        request = self.client.get(user_change_url)
        request.user = non_admin_user
        admin = CustomUserAdmin(User, None)

        self.assertEqual(request.status_code, 302)
        self.assertFalse(admin.has_view_permission(request))
        self.assertFalse(admin.has_add_permission(request))
        self.assertFalse(admin.has_change_permission(request))
        self.assertFalse(admin.has_delete_permission(request))

    def test_custom_group_admin_non_superuser_permissions(self):
        non_admin_user = User.objects.create_user(
            username=fake.user_name(), password=fake.password(), email=fake.email()
        )

        self.client.force_login(non_admin_user)

        group_change_url = reverse("admin:auth_group_add")
        request = self.client.get(group_change_url)
        request.user = non_admin_user
        admin = CustomGroupAdmin(Group, None)

        self.assertEqual(request.status_code, 302)
        self.assertFalse(admin.has_view_permission(request))
        self.assertFalse(admin.has_add_permission(request))
        self.assertFalse(admin.has_change_permission(request))
        self.assertFalse(admin.has_delete_permission(request))
