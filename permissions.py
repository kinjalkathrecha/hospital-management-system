from rest_framework.permissions import BasePermission

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'PATIENT'

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'DOCTOR'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class IsStaffOrDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['STAFF', 'DOCTOR', 'ADMIN']