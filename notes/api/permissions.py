from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission to allow access to owners or admin users.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user and request.user.is_staff:
            return True

        # Otherwise, only the owner is allowed
        return obj.owner == request.user
