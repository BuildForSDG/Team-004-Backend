from sme_management.models import *
from user_management.models import User
from user_management.serializers import UserSerializer

from rest_framework import serializers


class SMESerializer(serializers.ModelSerializer):
    """Serializer for SME Model."""

    class Meta:
        model = SME
        fields = ('id', 'org_name')
        read_only_fields = ('id',)


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

        sme_user_model = self.Meta.model

        user_data = validated_data.pop('user')
        payload = {'role': 'SME_USER'}
        user_data.update(payload)
        new_user = User.objects.create_user(**user_data)

        sme_data = validated_data.pop('sme')
        new_sme = SME.objects.create(**sme_data)

        return sme_user_model.objects.create(sme=new_sme, user=new_user)


# Call one create project
# Call two to create milestones
# If there's a project without milestones created, delete it ***

# First create project with document
# Then update the project with task list

class SMEProjectSerializer(serializers.ModelSerializer):
    """Serializer for SME Projects."""
    sme = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=SME.objects.all()
    )

    # TODO: What constitutes as an empty file? Do more research after MVP
    business_plan = serializers.FileField(allow_empty_file=True)
    cashflow_statement = serializers.FileField(allow_empty_file=True)
    income_statement = serializers.FileField(allow_empty_file=True)
    balance_sheet = serializers.FileField(allow_empty_file=True)

    class Meta:
        model = SMEProject
        fields = (
            'id', 'project_name', 'business_plan',
            'investment_tenure_end_date', 'cashflow_statement',
            'income_statement', 'balance_sheet',
            'category', 'amount_required', 'equity_offering',
            'sme', 'status'
        )
        read_only_fields = ('id', 'status',)


class SMEProjectMilestonesSerializer(serializers.ModelSerializer):
    """Serializer for SMEProjectMilestones Model without document"""

    class Meta:
        model = SMEProjectMilestones
        fields = (
            'id', 'name', 'description',
            'proof_of_completion',
            'amount_required', 'sme_project',
            'sme'
        )
        read_only_fields = ('id', 'proof_of_completion',)


class SMEProjectMilestonesDocSerializer(serializers.ModelSerializer):
    """Serializer for SMEProjectMilestones Model with document"""

    class Meta:
        model = SMEProjectMilestones
        fields = (
            'id', 'proof_of_completion', 'status', 'sme_project'
        )
