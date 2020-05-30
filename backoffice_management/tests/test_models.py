from django.test import TestCase
from django.contrib.auth import get_user_model
from backoffice_management.models import BackofficeUser


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


class BackofficeUserModelTests(TestCase):
    """Backoffice user model test"""

    def test_backoffice_user_created_successfully(self):
        """Test that backoffice user created successfully."""

        BackofficeUser.objects.create(
            user=create_sample_user()
        )
        backoffice_user = BackofficeUser.objects.all()

        self.assertEqual(len(backoffice_user), 1)
