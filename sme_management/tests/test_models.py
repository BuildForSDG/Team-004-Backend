from django.test import TestCase
from django.contrib.auth import get_user_model
from sme_management.models import *


def create_sample_sme(org_name='Andela', address='Ikorodu Rd'):
    """Create and return sample sme."""
    return SME.objects.create(org_name=org_name, address=address)


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


class SMEManagementModelTests(TestCase):

    def test_sme_created_successfully(self):
        """Test that sme is created successfully"""

        sme = create_sample_sme()
        self.assertEqual(str(sme), sme.org_name)


def test_sme_user_created_successfully(self):
    """Test that sme user is created successfully"""

    SMEUser.objects.create(
        sme=create_sample_sme(),
        user=create_sample_user()
    )

    sme_users = SMEUser.objects.all()

    self.assertEqual(len(sme_users), 1)
