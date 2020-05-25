from investor_management.models import *
from user_management.models import User
from user_management.serializers import UserSerializer

from rest_framework import serializers


class InvestorOrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Investor Organization."""

    class Meta:
        model = InvestorOrganization
        fields = ('id', 'org_name', 'address')
        read_only_fields = ('id',)


class ManageInvestorUserSerializer(serializers.ModelSerializer):
    """Serializer to Manage Investor Users."""

    investor_org = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True
    )
    user = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True
    )

    class Meta:
        model = InvestorUser
        fields = ('id', 'investor_org', 'user')
        read_only_fields = ('id',)


class CreateInvestorUserSerializer(ManageInvestorUserSerializer):
    investor_org = InvestorOrganizationSerializer(many=False)
    user = UserSerializer(many=False)

    def create(self, validated_data):
        """Create Investor User."""

        user_data = validated_data.pop('user')
        payload = {'role': 'INVESTOR_USER'}
        user_data.update(payload)
        new_user = User.objects.create_user(**user_data)

        investor_org_data = validated_data.pop('investor_org')
        new_investor_org = InvestorOrganization.objects.create(**investor_org_data)

        investor_user_model = self.Meta.model

        return investor_user_model.objects.create(investor_org=new_investor_org, user=new_user)
