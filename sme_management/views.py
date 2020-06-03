from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets

from django.db.models import Q

from sme_management.serializers import *
from sme_management import permissions


class CreateSMEUserView(generics.CreateAPIView):
    """Create a SME user in the system"""
    serializer_class = CreateSMEUserSerializer
    queryset = SMEUser.objects.all()


class ManageSMEUserView(generics.RetrieveAPIView):
    """Manage SME Users in the database"""

    queryset = SMEUser.objects.all()
    serializer_class = ManageSMEUserSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        """Retrieve the SMEUser for the authenticated user"""
        return self.queryset.filter(user=self.request.user)


class SMEProjectAPIView(APIView):
    """
    API View to create projects with documents -
    cashflow statement, income statement &
    balance sheets
    """

    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = SMEProjectSerializer
    parser_class = (FileUploadParser,)
    search_fields = ('status',)

    def post(self, request, *args, **kwargs):

        incomplete_project_exists = SMEProject.objects.filter(~Q(status='COMPLETED')).exists()
        if incomplete_project_exists:
            return Response(data="An incomplete project still exists",
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # TODO: In the future, we would want to make a separation between
    #  how we get COMPLETED, IN_PROGRESS and UNAPPROVED projects
    #  For now, we just return everything in one call
    #  There might be a solution to this with search_fields. Confirm
    def get(self, request, *args, **kwargs):
        # Get sme, then filter projects by sme
        # user linked to sme user, which is linked to sme

        user = self.request.user
        sme_user = user.smeuser
        sme = None

        if sme_user:
            sme = sme_user.sme

        if sme:
            projects = SMEProject.objects.filter(sme=sme)

            # Delete projects without any milestones
            for project in projects:
                if not SMEProjectMilestones.objects.filter(sme_project=project):
                    project.delete()

            projects = SMEProject.objects.filter(sme=sme)

            serializer = self.serializer_class(projects, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# TODO: Restrict this endpoint to just INVESTOR_USERs,
#  then test it in investor_management
class SMEProjectsListAPIView(generics.ListAPIView):
    serializer_class = SMEProjectSerializer
    queryset = SMEProject.objects.filter(~Q(status='COMPLETED'))
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.ViewProjectTimeline,
        IsAuthenticated
    )


class SMEProjectMilestoneViewSet(viewsets.ModelViewSet):
    """
    View to allow creation of single or multiple
    milestones for a project
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = SMEProjectMilestones.objects.all()
    serializer_class = SMEProjectMilestonesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """Use this to retrieve the milestones for a particular project"""
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return self.queryset.filter(sme_project=project_id)
        return self.queryset


# TODO: Ensure updates can only happen for milestones an SME_USER has access to
class SMEProjectMilestoneAPIView(APIView):
    lookup_url_kwarg = 'id'
    parser_class = (FileUploadParser,)
    queryset = SMEProjectMilestones.objects.all()
    serializer_class = SMEProjectMilestonesDocSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, permissions.UploadProofForMilestone)

    def patch(self, request, *args, **kwargs):
        existing_milestone = SMEProjectMilestones.objects.get(id=kwargs['id'])
        self.check_object_permissions(request, existing_milestone)
        serializer = self.serializer_class(existing_milestone, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
