from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from six import text_type


class ActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.id) + text_type(timestamp) + text_type(user.is_active)


activation_token = ActivationTokenGenerator()


def send_email(request, user):
    protocol = "https" if request.is_secure() else "http"
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.id))
    url = reverse("accounts:verify")
    token = uid + "." + activation_token.make_token(user)
    activation_link = protocol + "://" + domain + url + "?token=" + token
    subject = "Account Verification"
    body = (
        "Hi, "
        + user.first_name
        + " "
        + user.last_name
        + "\nWelcome to DIU CPC. Click this link to verify your account.\n"
        + activation_link
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, body, f"DIU CPC <{from_email}>", [user.email])
    msg.send()


def profile_photo_path(instance, filename):
    extension = filename.split(".")[-1]
    path = instance.username + "." + extension
    return f"profile_photo/{path}"
