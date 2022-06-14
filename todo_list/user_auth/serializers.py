from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class NullSerializer(serializers.ModelSerializer):
    pass


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'password']
        read_only_fields = ['id', 'is_active', 'password']


# Login Serializer
class LoginSerializer(UserSerializer):
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
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")
        validated_data["user"] = user

        return validated_data

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields


# Signup Serializer
class SignupSerializer(UserSerializer):
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

    def validate(self, data):
        """
            validate username & password for sign-up
        """
        username = data.get("username", "")
        password = data.get("password", "")
        confirm_password = data.get("confirm_password", "")

        # password confirmation check
        if password != confirm_password:
            msg = _("Passwords didn't match")
            raise serializers.ValidationError(msg, code="authorization")

        # username uniqueness check
        if User.objects.filter(username=username).exists():
            msg = _(f"{username} User already exists")
            raise serializers.ValidationError(msg, code="authorization")

        validate_password(password)

        User.objects.create_user(username=username, password=password)
        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

        data["user"] = user
        return data

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['confirm_password']
        read_only_fields = UserSerializer.Meta.read_only_fields + ['confirm_password']
