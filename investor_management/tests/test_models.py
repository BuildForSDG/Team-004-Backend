from django.test import TestCase
from django.contrib.auth import get_user_model
from investor_management.models import *


def create_sample_investor_org(org_name='XX Holdings', address='Nigeria'):
    """Create and return a sample investor"""

    return InvestorOrganization.objects.create(
        org_name=org_name,
        address=address
    )


def create_sample_user(email='Test@email.com',
                       first_name='Test', last_name='User'):
    """Create and return a sample user"""

    return get_user_model().objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_no='09090909121',
        password='12345678**'
    )


class InvestorManagementModelTests(TestCase):
    def test_create_investor_organization_is_successful(self):
        """Test creating investor organization is successful"""

        investor_org = create_sample_investor_org()
        self.assertEqual(str(investor_org), investor_org.org_name)

    def test_investor_user_created_successfully(self):
        """Test that investor user is created successfully"""

        InvestorUser.objects.create(
            investor_org=create_sample_investor_org(),
            user=create_sample_user()
        )

        investor_users = InvestorUser.objects.all()

        self.assertEqual(len(investor_users), 1)
