import os

from django.core.files import File
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings

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


def create_sample_project_with_documents():
    """Create a sample project with documents."""

    # Create a sample test file
    fpath = "testfile.txt"
    file = open(fpath, "w")
    file.write("Hello World")
    file.close()
    file = open(fpath, "r")
    f = File(file)

    sme = create_sample_sme()
    return SMEProject.objects.create(
        project_name="Sample Project",
        project_description="Sample Desc",
        business_plan=f,
        investment_tenure_end_date="2021-06-15",
        cashflow_statement=f,
        income_statement=f,
        balance_sheet=f,
        category='',
        amount_required=30,
        amount_raised=0,
        equity_offering=15,
        status="UNAPPROVED",
        sme=sme
    ), fpath


def create_sample_project_without_documents():
    """Create a sample project with documents."""

    sme = create_sample_sme()
    return SMEProject.objects.create(
        project_name="Sample Project",
        project_description="Sample Desc",
        investment_tenure_end_date="2021-06-15",
        category='',
        amount_required=30,
        amount_raised=0,
        equity_offering=15,
        status="UNAPPROVED",
        sme=sme
    )


class SMEManagementModelTests(TestCase):

    # def setUp(self):
    #     settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, "media-tmp")

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

    def test_sme_project_created_successfully(self):
        """Test that sme project is created successfully"""

        sme_project, fpath = create_sample_project_with_documents()

        self.assertEqual(sme_project.project_name, "Sample Project")
        self.assertEqual(sme_project.status, "UNAPPROVED")
        self.assertTrue(
            os.path.exists(settings.BASE_DIR + sme_project.business_plan.url))
        self.assertTrue(
            os.path.exists(settings.BASE_DIR + sme_project.cashflow_statement.url))
        self.assertTrue(
            os.path.exists(settings.BASE_DIR + sme_project.income_statement.url))
        self.assertTrue(
            os.path.exists(settings.BASE_DIR + sme_project.balance_sheet.url))

        os.remove(fpath)
        os.remove(settings.BASE_DIR + sme_project.business_plan.url)
        os.remove(settings.BASE_DIR + sme_project.cashflow_statement.url)
        os.remove(settings.BASE_DIR + sme_project.income_statement.url)
        os.remove(settings.BASE_DIR + sme_project.balance_sheet.url)

    def test_sme_project_milestones_created_successfully(self):
        """Test that an sme project milestone is created successfully"""

        sme_project = create_sample_project_without_documents()
        project_milestone = SMEProjectMilestones.objects.create(
            name="Sample Milestone",
            description="Sample Desc",
            amount_required=27,
            sme_project=sme_project,
            sme=sme_project.sme
        )

        self.assertEqual(project_milestone.name, "Sample Milestone")
