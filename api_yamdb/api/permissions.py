from rest_framework.permissions import BasePermission


class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'admin' or request.user.is_staff == True:
                return True
        else:
            return False