from rest_framework.permissions import BasePermission, SAFE_METHODS


class OpenListPrivateDetailPermission(BasePermission):
    """
    Permission class that provides mixed access levels:

    - Allows unrestricted access (including unauthenticated users) to the list view (GET /objects/).
    - Allows access to retrieve (GET /objects/{id}/) and other safe methods only for authenticated users.
    - Allows modification actions (POST, PUT, PATCH, DELETE) only for admin users (is_staff=True).

    This is useful for APIs where general data visibility is allowed,
    but detailed views and modifications require higher permissions.
    """

    def has_permission(self, request, view):
        if view.action == "list":
            return True

        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated

        return request.user and request.user.is_staff
