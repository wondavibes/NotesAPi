from rest_framework.permissions import BasePermission, SAFE_METHODS
from notes.models import NoteAccess

class NotePermission(BasePermission):

    def has_object_permission(self, request, view, obj): # type: ignore
        user = request.user

        if user.is_staff:
            return True

        # Owner shortcut
        if obj.owner == user:
            return True

        # Fetch NoteAccess once
        access = NoteAccess.objects.filter(
            note=obj,
            user=user
        ).first()

        # SAFE METHODS (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            if obj.visibility == obj.Visibility.PUBLIC:
                return True

            return access is not None

        # EDIT METHODS
        if request.method in ["PUT", "PATCH"]:
            return access and access.access_level == "edit"

        # DELETE → owner only (already handled above)
        if request.method == "DELETE":
            return False

        return False
