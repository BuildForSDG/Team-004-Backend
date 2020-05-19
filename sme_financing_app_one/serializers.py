from rest_framework import serializers
from sme_financing_app_one import models


class ProfileSerializer(serializers.ModelSerializer):
    """Create User Profile Serializer."""
    class Meta:
        """Create user."""

        model = models.UserProfile
        fields = ('id', 'email', 'first_name', 'last_name',
                  'password', 'date_joined', 'phone_no')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    @classmethod
    def create(self, validated_data):
        """Create and return a new user."""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_joined=['date_joined'],
            phone_no=validated_data['phone_no'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account."""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)
