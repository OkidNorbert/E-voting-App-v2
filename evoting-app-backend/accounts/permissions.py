from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Allow any admin user for any method.
    Used for general admin-only views.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_user)


class IsAdminWriteUser(BasePermission):
    """
    Allow only admins with write access (excludes AUDITOR).
    Used for state-changing admin actions.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated and request.user.is_admin_user):
            return False
        
        # Auditor should only have read access
        if request.user.role == request.user.Role.AUDITOR:
            return request.method in ("GET", "HEAD", "OPTIONS")
        
        return True


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_super_admin)


class IsVerifiedVoter(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_voter_user
            and request.user.is_verified
        )


class IsAdminOrReadOnlyVoter(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_admin_user:
            # Auditor is read-only
            if request.user.role == request.user.Role.AUDITOR:
                return request.method in ("GET", "HEAD", "OPTIONS")
            return True

        if request.user.is_voter_user and request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        return False
