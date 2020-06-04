from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from sme_management.tests.test_sme_apis import \
    create_sample_sme_project_with_milestones, \
    create_user, create_sample_sme

GET_ALL_SME_PROJECTS = reverse('sme_management:sme_project_timeline')


class InvestorManagementAPITests(TestCase):
    """Test all endpoints that will be called by Investor Users"""

    def setUp(self):
        self.user = create_user(
            first_name='Ayo',
            last_name='User',
            phone_no='09001234123',
            email='ayo@user.com',
            password='testing',
            role='INVESTOR_USER'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_all_sme_projects_for_investor_user_is_successful(self):
        """Test that an investor user can see all sme projects"""

        # Create two smes
        sme1 = create_sample_sme(org_name="Org 1", address="Addy 1")
        sme2 = create_sample_sme(org_name="Org 2", address="Addy 2")

        # Create two projects with milestones
        create_sample_sme_project_with_milestones(sme1)
        create_sample_sme_project_with_milestones(sme2)

        # Fetch & ensure it's successful
        res = self.client.get(GET_ALL_SME_PROJECTS)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
