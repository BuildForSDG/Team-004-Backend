import os

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.test import APIClient

from sme_management.models import *

CREATE_SME_PROJECT_URL = reverse('sme_management:sme_project_create')
CREATE_PROJECT_MILESTONES_URL = reverse('sme_management:smeprojectmilestones-list')
GET_ALL_SME_PROJECTS = reverse('sme_management:sme_project_timeline')


def get_update_milestone_url(milestone_id):
    return reverse('sme_management:sme_project_milestone', kwargs={'id': milestone_id})


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_sample_sme(org_name='Andela', address='Ikorodu Rd'):
    """Create and return sample sme."""
    return SME.objects.create(org_name=org_name, address=address)


def create_sme_user(user, sme=create_sample_sme()):
    return SMEUser.objects.create(sme=sme, user=user)


def create_sample_milestone_for_sme_project(sme_project):
    return SMEProjectMilestones.objects.create(
        name="Sample Milestone 1",
        description="Sample Description 1",
        amount_required=30,
        sme_project=sme_project,
        sme=sme_project.sme
    )


def create_sample_sme_project_with_milestones(sme):
    """Create and return sample sme project."""
    sme_project = SMEProject.objects.create(
        project_name="Sample Project",
        project_description="Sample Desc",
        investment_tenure_end_date="2021-06-15",
        category="Technology",
        amount_required=30,
        amount_raised=0,
        equity_offering=15,
        status="UNAPPROVED",
        sme=sme
    )

    milestone = create_sample_milestone_for_sme_project(sme_project)
    return sme_project, milestone


def create_sample_sme_project_without_milestones(sme):
    """Create and return sample sme project."""
    sme_project = SMEProject.objects.create(
        project_name="Sample Project",
        project_description="Sample Desc",
        investment_tenure_end_date="2021-06-15",
        category="Technology",
        amount_required=30,
        amount_raised=0,
        equity_offering=15,
        status="UNAPPROVED",
        sme=sme
    )

    return sme_project


def get_create_sme_project_payload():
    sme = create_sample_sme()
    payload = {
        'project_name': "Sample Project",
        'project_description': "Sample Desc",
        'investment_tenure_end_date': '2021-06-15',
        'category': 'Technology',
        'amount_required': 30,
        'amount_raised': 0,
        'equity_offering': 15,
        'project_completion_status': 'UNAPPROVED',
        'sme': sme.id
    }

    return payload, sme


def get_create_milestone_payload():
    sme = create_sample_sme()
    sme_project = create_sample_sme_project_without_milestones(sme=sme)
    payload = [
        {
            "name": "Sample Milestone 1",
            "description": "Sample Description 1",
            "amount_required": 30,
            "sme_project": sme_project.id,
            "sme": sme_project.sme.id
        },
        {
            "name": "Sample Milestone 2",
            "description": "Sample Description 2",
            "amount_required": 30,
            "sme_project": sme_project.id,
            "sme": sme_project.sme.id
        }
    ]

    return payload, sme_project


def generate_sample_file():
    """Create a sample test file"""
    fpath = settings.MEDIA_ROOT + "/testfile.txt"
    file = open(fpath, "w")
    file.write("Hello World")
    file.close()

    return file


class SMEManagementAPITests(TestCase):
    """All SME Project Tests"""

    def setUp(self):
        self.user = create_user(
            first_name='Ayo',
            last_name='User',
            phone_no='09001234123',
            email='ayo@user.com',
            password='testing',
            role='SME_USER'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_sme_project(self):
        """Test sme project creation endpoint for authenticated users"""

        payload, sme = get_create_sme_project_payload()
        create_sme_user(user=self.user, sme=sme)

        file = generate_sample_file()
        file_path = file.name
        f = open(file_path, "rb")

        payload['business_plan'] = f
        payload['cashflow_statement'] = f
        payload['income_statement'] = f
        payload['balance_sheet'] = f

        res = self.client.post(CREATE_SME_PROJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(sme.id, res.data['sme'])
        self.assertTrue(
            os.path.exists(settings.BASE_DIR + res.data['business_plan']))
        self.assertTrue(
            os.path.exists(settings.BASE_DIR + res.data['cashflow_statement']))
        self.assertTrue(
            os.path.exists(settings.BASE_DIR + res.data['income_statement']))
        self.assertTrue(
            os.path.exists(settings.BASE_DIR + res.data['balance_sheet']))

        os.remove(file_path)
        os.remove(settings.BASE_DIR + res.data['business_plan'])
        os.remove(settings.BASE_DIR + res.data['cashflow_statement'])
        os.remove(settings.BASE_DIR + res.data['income_statement'])
        os.remove(settings.BASE_DIR + res.data['balance_sheet'])

    def test_create_sme_project_without_sme_fails(self):
        """Test that trying to create an sme project that isn't attached to an sme fails"""

        payload, sme = get_create_sme_project_payload()
        payload.pop('sme', None)

        create_sme_user(user=self.user, sme=sme)
        sme.delete()

        file = generate_sample_file()
        file_path = file.name
        f = open(file_path, "rb")

        payload['business_plan'] = f
        payload['cashflow_statement'] = f
        payload['income_statement'] = f
        payload['balance_sheet'] = f

        res = self.client.post(CREATE_SME_PROJECT_URL, payload)

        self.assertNotIn('sme', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fetching_sme_projects_with_milestone_successful(self):
        """
        Test that fetching sme projects for an sme is successful
        Also test that an sme can't fetch projects for a different sme

        Test that all sme projects that are returned have milestones
        """

        sme1 = create_sample_sme(org_name="WeFinance", address="Home")
        create_sample_sme_project_with_milestones(sme=sme1)
        create_sample_sme_project_with_milestones(sme=sme1)

        # Create sme user from user and sme1
        create_sme_user(user=self.user, sme=sme1)

        sme2 = create_sample_sme(org_name="Jamski")
        create_sample_sme_project_with_milestones(sme=sme2)

        res = self.client.get(CREATE_SME_PROJECT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for project in res.data:
            self.assertEqual(project['sme'], sme1.id)

    def test_fetching_sme_projects_without_milestones_fails(self):
        """
        Test that try to fetch sme projects without milestones
        lazy deletes the project and returns nothing to the client
        """

        sme = create_sample_sme(org_name="WeFinance", address="Home")

        # Create sme user from user and sme
        create_sme_user(user=self.user, sme=sme)

        create_sample_sme_project_with_milestones(sme=sme)
        sme_project2 = create_sample_sme_project_without_milestones(sme=sme)

        res = self.client.get(CREATE_SME_PROJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for project in res.data:
            self.assertNotEqual(project['id'], sme_project2.id)

    def test_creating_milestones_for_project_is_successful(self):
        """Test creating milestones for project is successful"""

        payload, sme_project = get_create_milestone_payload()

        res = self.client.post(CREATE_PROJECT_MILESTONES_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload[0]['name'], res.data[0]['name'])
        self.assertEqual(payload[1]['name'], res.data[1]['name'])
        self.assertEqual(res.data[0]['sme_project'], sme_project.id)
        self.assertEqual(res.data[1]['sme_project'], sme_project.id)

    def test_creating_milestones_without_project_fails(self):
        """
        Test that creating dangling milestones fails
        All milestones must be assigned to a project
        """

        payload, sme_project = get_create_milestone_payload()
        payload[0].pop('sme_project', None)
        payload[1].pop('sme_project', None)

        sme_project.delete()

        res = self.client.post(CREATE_PROJECT_MILESTONES_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_sme_projects_for_sme_user_fails(self):
        """Test that an sme user cannot see all the sme projects that need financing"""

        # Create two smes
        sme1 = create_sample_sme(org_name="Org 1", address="Addy 1")
        sme2 = create_sample_sme(org_name="Org 2", address="Addy 2")

        # Create two projects with milestones
        create_sample_sme_project_with_milestones(sme1)
        create_sample_sme_project_with_milestones(sme2)

        # Fetch & ensure it's successful
        res = self.client.get(GET_ALL_SME_PROJECTS)

        self.assertEqual(self.user.role, 'SME_USER')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_patch_request_on_milestone_fails(self):
        """
        Test that an SME_USER cannot update a milestone that does
        not belong to the SME_USER's SME
        """
        sme1 = create_sample_sme(org_name="Org 1", address="Addy 1")

        # Create sme project with milestones for new user
        sme_project, milestone = create_sample_sme_project_with_milestones(sme1)

        # Only doing this because sme_project will be an unused variable otherwise
        print(sme_project)

        # Try updating it with self user
        payload = {'status': 'COMPLETED'}
        url = get_update_milestone_url(milestone.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], 'You do not have access to this milestone')

    def test_upload_proof_docs_for_milestone_is_successful(self):
        """Test uploading documents for smeproject milestone is successful"""
        sme1 = create_sample_sme(org_name="Org 1", address="Addy 1")

        create_sme_user(self.user, sme1)
        sme_project, milestone = create_sample_sme_project_with_milestones(sme1)

        # Only doing this because sme_project will be an unused variable otherwise
        print(sme_project)

        file = generate_sample_file()
        file_path = file.name
        f = open(file_path, "rb")

        payload = {'proof_of_completion': f}
        url = get_update_milestone_url(milestone.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(
            os.path.exists(settings.BASE_DIR + res.data['proof_of_completion']))

        os.remove(file_path)
        os.remove(settings.BASE_DIR + res.data['proof_of_completion'])

    def test_update_milestone_status_is_successful(self):
        """Test updating status for smeproject milestone is successful"""

        sme1 = create_sample_sme(org_name="Org 1", address="Addy 1")

        create_sme_user(self.user, sme1)
        sme_project, milestone = create_sample_sme_project_with_milestones(sme1)

        # Only doing this because sme_project will be an unused variable otherwise
        print(sme_project)

        payload = {'status': 'COMPLETED'}
        url = get_update_milestone_url(milestone.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(milestone.status, 'NOT_STARTED')

        milestone.refresh_from_db()
        self.assertTrue(milestone.status, 'COMPLETED')
