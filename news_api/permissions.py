# permissions.py

from rest_framework import permissions

class IsReporterOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow reporters to edit their own articles.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the reporter of the article.
        return obj.reporter == request.user
