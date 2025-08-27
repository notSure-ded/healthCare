from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Read-only access is allowed for any authenticated user.
    """
    def has_permission(self, request, view):
        # Allow all authenticated users to perform safe methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        # For unsafe methods (POST, PUT, DELETE), only allow if the user is staff.
        return request.user and request.user.is_staff
