from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class UserInfoSerializer(ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "role",
            "profile_photo",
        ]


class UserCreateSerializer(ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "password2",
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Password doesn't match"})
        return data

    def save(self, **kwargs):
        self.validated_data.pop("password2")
        user = User(is_active=False, **self.validated_data)
        user.set_password(self.validated_data["password"])
        user.save()
        return user
