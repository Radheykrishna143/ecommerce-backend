from rest_framework.permissions import BasePermission, SAFE_METHODS


class isAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # allow get head options for everyone
        if request.method in SAFE_METHODS:
            return True

        # only admin role can modify
        return request.user.is_authenticated and request.user.role == "admin"
