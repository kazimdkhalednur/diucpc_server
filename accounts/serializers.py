from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]


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
            raise serializers.ValidationError("Password doesn't match")
        return data

    def save(self, **kwargs):
        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError("Email already exists")

        self.validated_data.pop("password2")
        user = User(**self.validated_data)
        user.set_password(self.validated_data["password"])
        user.save()
        return user
