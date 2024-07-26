from rest_framework.permissions import BasePermission

from JobSeekerApp.models import ApplyRequest


class ApplyRequestPermission(BasePermission):
    def has_object_permission(self, request, view, obj: ApplyRequest):
        if request.user.is_employer:
            return request.user == obj.job_advertisement.employer
        return request.user == obj.job_seeker
