from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed

from .tokens import get_token_for_user


class NullSerializer(serializers.ModelSerializer):
    pass


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'password']
        read_only_fields = ['id', 'is_active', 'password']


# JWT Token Serializer
class AuthTokenSerializer(UserSerializer):
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, instance):
        """
            generate JWT token for user
        """
        return get_token_for_user(instance)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['auth_token']


# Login Serializer
class LoginSerializer(AuthTokenSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )

    def validate(self, validated_data):
        """
            validate username & password before sign-in
        """
        username = validated_data.get("username", "")
        password = validated_data.get("password", "")

        if username and password:
            # password validation
            validate_password(password)
            # authentication validation
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                raise AuthenticationFailed("Unable to log in with provided credentials.")
            if not user.is_active:
                raise AuthenticationFailed("Account disabled, contact admin")
        else:
            raise AuthenticationFailed('Must include "username" and "password".')

        return user

    class Meta(AuthTokenSerializer.Meta):
        fields = AuthTokenSerializer.Meta.fields


# Signup Serializer
class SignupSerializer(AuthTokenSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "new_password"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )
    confirm_password = serializers.CharField(
        label=_("Confirm Password"),
        style={"input_type": "confirm_password"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )

    def validate(self, validated_data):
        """
            validate username & password for sign-up
        """
        username = validated_data.get("username", "")
        password = validated_data.get("password", "")
        confirm_password = validated_data.get("confirm_password", "")

        # password confirmation check
        if password != confirm_password:
            raise AuthenticationFailed("Passwords didn't match")

        # username uniqueness check
        if User.objects.filter(username=username).exists():
            raise AuthenticationFailed(f"{username} User already exists")

        validate_password(password)
        validated_data.pop("confirm_password", "")
        return validated_data


    class Meta(AuthTokenSerializer.Meta):
        fields = AuthTokenSerializer.Meta.fields + ['confirm_password']
        read_only_fields = AuthTokenSerializer.Meta.read_only_fields + ['confirm_password']
