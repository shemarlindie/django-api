from django.urls import reverse
from rest_framework.permissions import BasePermission


class IsCreate(BasePermission):
    """
    Allow access to "create" action on the view
    """
    def has_permission(self, request, view):
        return view.action == 'create'

    def has_object_permission(self, request, view, obj):
        return False


class IsStaff(BasePermission):
    """
    Allow staff to perform any operation
    """
    def has_permission(self, request, view):
        return all([request.user.is_authenticated, request.user.is_staff])

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwnUserProfile(BasePermission):
    """
    Allow any user to modify their own profile
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # prevent access to user list
        is_list_url = request.get_full_path() == reverse('auth_api:users-list')
        if is_list_url:
            return False

        # WORKAROUND: for some reason has_object_permission isn't called for DELETE
        # if view.action == 'destroy':
        #     return view.kwargs['pk'] == request.user.id

        return True

    def has_object_permission(self, request, view, obj):
        return obj == request.user
