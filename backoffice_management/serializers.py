from backoffice_management.models import BackofficeUser
from user_management.models import User
from user_management.serializers import UserSerializer

from rest_framework import serializers


class ManageBackofficeUserSerializer(serializers.ModelSerializer):
    """
    This serializer was created to ensure that user details
    won't be editable via the backoffice/user endpoint
    """

    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = BackofficeUser
        fields = ('id', 'user')
        read_only_fields = ('id',)


class CreateBackOfficeUserSerializer(ManageBackofficeUserSerializer):
    """Serializer for Backoffice User."""

    user = UserSerializer(many=False)

    def create(self, validated_data):
        """Create Backoffice User."""

        backoffice_user_model = self.Meta.model

        user_data = validated_data.pop('user')
        payload = {'role': 'BACKOFFICE_USER'}
        user_data.update(payload)
        new_user = User.objects.create_user(**user_data)

        return backoffice_user_model.objects.create(user=new_user)
