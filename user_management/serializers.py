from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer to provide login object to client."""

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'first_name', 'last_name', 'phone_no',
            'email', 'password', 'role'
        )

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'role': {
                'read_only': True
            },
            'id': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        """ Create and return a new user."""

        user_model = self.Meta.model
        user = user_model.objects.create_user(
            **validated_data
        )

        return user

    def update(self, instance, validated_data):
        """Update an authenticated user."""

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object."""
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate user."""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )

            if not user:
                msg = _("Unable to authenticate with provided credentials")
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _("Must include email and password to authenticate")
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
