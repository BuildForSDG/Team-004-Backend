from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from sme_management.models import SME
from investor_management.models import InvestorOrganization

CREATE_SME_USER_URL = reverse('sme_management:sme_user_create')
CREATE_INVESTOR_USER_URL = reverse('investor_management:investor_user_create')
AUTHENTICATE_URL = reverse('user_management:login')


def get_create_user_payload():
    payload = {
        'user': {
            'first_name': 'Ayo',
            'last_name': 'User',
            'phone_no': '09001234123',
            'email': 'ayo@user.com',
            'password': 'testing',
        }
    }

    return payload


def get_login_user_payload():
    payload = {
        'email': 'ayo@user.com',
        'password': 'testing'
    }
    return payload


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class CreateUserAPITests(TestCase):
    """
    Test creation of all users

    Current user types that exist include:
    SME_USER, INVESTOR_USER & BACKOFFICE_USER
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_sme_user_is_successful(self):
        """Test creating SME_USER is successful."""
        payload = get_create_user_payload()
        payload['sme'] = {
            'org_name': 'Test Org'
        }

        res = self.client.post(CREATE_SME_USER_URL, payload, format='json')
        sme = SME.objects.get(**res.data['sme'])
        user = get_user_model().objects.get(**res.data['user'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload['sme']['org_name'], sme.org_name)
        self.assertEqual(payload['user']['first_name'], user.first_name)
        self.assertEqual(payload['user']['last_name'], user.last_name)
        self.assertEqual('SME_USER', user.role)
        self.assertTrue(user.check_password(payload['user']['password']))
        self.assertNotIn('password', res.data)

    def test_create_investor_user_is_successful(self):
        """Test creating INVESTOR_USER is successful."""
        payload = get_create_user_payload()
        payload['investor_org'] = {
            'org_name': 'Test Org'
        }

        res = self.client.post(CREATE_INVESTOR_USER_URL, payload, format='json')
        investor_org = InvestorOrganization.objects.get(**res.data['investor_org'])
        user = get_user_model().objects.get(**res.data['user'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload['investor_org']['org_name'], investor_org.org_name)
        self.assertEqual(payload['user']['first_name'], user.first_name)
        self.assertEqual(payload['user']['last_name'], user.last_name)
        self.assertEqual('INVESTOR_USER', user.role)
        self.assertTrue(user.check_password(payload['user']['password']))
        self.assertNotIn('password', res.data)

    def test_creating_duplicate_user_fails(self):
        """
        Tests that a user whose email address has been registered
        with cannot be used to register again
        """

        payload = get_create_user_payload()
        create_user(**payload['user'])

        payload['sme'] = {
            'org_name': 'Test Org'
        }

        res = self.client.post(CREATE_SME_USER_URL, payload, format='json')
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)


class AuthenticateUserAPITests(TestCase):
    """
    Test user can login
    Test user gets role, token and user_id in response
    """

    def setUp(self):
        self.client = APIClient()

    def test_token_and_role_returned_after_user_login(self):
        """

        This test applies to ALL USERs

        Test that role like SME_USER or
        INVESTOR_USER or BACKOFFICE_USER is returned

        Test that token is returned
        """

        payload = get_create_user_payload()['user']
        payload['role'] = 'SME_USER'
        create_user(**payload)

        res = self.client.post(AUTHENTICATE_URL, get_login_user_payload())
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)
        self.assertEqual(res.data['role'], payload['role'])

    def test_login_fails_for_invalid_credentials(self):
        """
        Test that login fails for invalid credentials
        This test only tests for SME_USER
        The assumption is that if it works for one, it works for all
        """

        payload = get_create_user_payload()['user']
        payload['role'] = 'SME_USER'
        create_user(**payload)

        req_payload = get_login_user_payload()
        req_payload['password'] = 'chowing'

        res = self.client.post(AUTHENTICATE_URL, req_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_login_fails_for_nonexistent_user(self):
        """Test that api fails when a user that doesn't exist tries to login"""

        payload = get_login_user_payload()

        res = self.client.post(AUTHENTICATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
