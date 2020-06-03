from rest_framework import permissions
from sme_management.models import SMEUser


class ViewProjectTimeline(permissions.BasePermission):
    """Allow only INVESTOR_USERs to views all projects that require financing"""

    message = 'You do not have permission to see timeline'

    def has_permission(self, request, view):
        """Check timeline is requested by investor or backoffice user"""
        print(request.user.role)
        print(view)
        permitted = request.user.role == 'INVESTOR_USER' or request.user.role == 'BACKOFFICE_USER'
        if not permitted:
            print(self.message)

        return permitted


class UploadProofForMilestone(permissions.BasePermission):
    """Allow SME_USERs only upload proof for milestones they have access to"""

    message = 'You do not have access to this milestone'

    def has_object_permission(self, request, view, obj):
        """Check user is trying to update a milestone they have access to"""
        sme = obj.sme
        exists = SMEUser.objects.filter(sme=sme, user=request.user).exists()
        if not exists:
            print(self.message)

        return exists
