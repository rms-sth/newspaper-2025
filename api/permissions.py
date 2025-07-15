from rest_framework import permissions

class IsStaffOrOwner(permissions.BasePermission):
    """
    Custom permission to allow only staff users or the owner of an object to edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS requests for anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow staff users to edit/delete any object
        if request.user and request.user.is_staff:
            return True

        # Allow the owner of the object to edit/delete it
        return obj.user == request.user