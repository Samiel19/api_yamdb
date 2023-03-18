from rest_framework.permissions import BasePermission, SAFE_METHODS

from rest_framework import permissions


class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'admin' or request.user.is_staff == True:
                return True
        else:
            return False


class IsAuthenticatedUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_staff
                 or request.user.role == 'admin'
                 or request.user.role == 'moderator'
                 or request.user == obj.author)
        )


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        
        if request.user.is_authenticated and request.user.role == "admin":
            return True
