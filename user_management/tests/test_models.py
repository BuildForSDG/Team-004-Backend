from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagementModelTests(TestCase):

    def test_create_user_with_correct_details_is_successful(self):
        """Test user is created when all the details are inserted."""

        email = 'test@gmail.com'
        fname = 'test'
        lname = 'user'
        phone_no = '08031231233'
        password = 'testingPass123'
        user = get_user_model().objects.create_user(
            fname,
            lname,
            phone_no,
            email,
            password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, fname)
        self.assertEqual(user.last_name, lname)
        self.assertTrue(user.check_password(password))

    def test_new_email_user_normalized(self):
        """Test new user's email is normalized."""
        email = 'test@GMAIL.COM'
        fname = 'test'
        lname = 'user'
        phone_no = '08031231233'
        password = 'testingPass123'

        user = get_user_model().objects.create_user(
            fname,
            lname,
            phone_no,
            email,
            password
        )

        self.assertEqual(user.email, email.lower())

    def test_create_user_without_email_raises_value_error(self):
        """Test that ValueError is raised when email is None."""

        email = None
        fname = 'test'
        lname = 'user'
        phone_no = '08031231233'
        password = 'testingPass123'

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                fname,
                lname,
                phone_no,
                email,
                password
            )

    def test_create_superuser_is_successful(self):
        """Test that superuser is created successfully with required details"""
        email = 'test@gmail.com'
        fname = 'test'
        lname = 'user'
        phone_no = '08031231233'
        password = 'testingPass123'

        user = get_user_model().objects.create_superuser(
            fname,
            lname,
            phone_no,
            email,
            password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
