from sme_management.models import *
from user_management.models import User
from user_management.serializers import UserSerializer

from rest_framework import serializers


class SMESerializer(serializers.ModelSerializer):
    """Serializer for SME Model."""

    class Meta:
        model = SME
        fields = ('id', 'org_name')
        extra_kwargs = {'id': {'read_only': True}}


class ManageSMEUserSerializer(serializers.ModelSerializer):
    """
    This serializer was created to ensure that user details
    won't be editable via the sme/user endpoint
    """

    sme = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True
    )
    user = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True
    )

    class Meta:
        model = SMEUser
        fields = ('id', 'sme', 'user')
        read_only_fields = ('id',)


class CreateSMEUserSerializer(ManageSMEUserSerializer):
    """Serializer for SME User."""

    sme = SMESerializer(many=False)
    user = UserSerializer(many=False)

    def create(self, validated_data):
        """Create SME User."""
        user_data = validated_data.pop('user')
        payload = {'role': 'SME_USER'}
        user_data.update(payload)
        new_user = User.objects.create_user(**user_data)

        sme_data = validated_data.pop('sme')
        new_sme = SME.objects.create(**sme_data)

        return SMEUser.objects.create(sme=new_sme, user=new_user)


class SMEProjectSerializer(serializers.ModelSerializer):
    """Serializer for SME Projects."""

    class Meta:
        model = SMEProject
        fields = ('business_plan',)
