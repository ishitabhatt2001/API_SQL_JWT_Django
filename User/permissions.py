from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a superuser
        return request.user.is_superuser

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a staffmember
        return request.user.is_staff_member
    
class IsUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a user
        return not request.user.is_staff_member and not request.user.is_superuser
    