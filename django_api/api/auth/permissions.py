from django.urls import reverse
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCreateView(BasePermission):
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
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsStaffOrReadOnly(BasePermission):
    """
    Only staff can edit, anyone else can view
    """
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user and request.user.is_staff)


class IsOwnUserProfile(BasePermission):
    """
    Allow any user to modify their own profile
    """
    def has_permission(self, request, view):
        # ensure authenticated
        if not (request.user and request.user.is_authenticated):
            return False

        # prevent access to user list
        if request.get_full_path() == reverse('auth_api:users-list'):
            return False

        # allow access to user detail
        if request.get_full_path() == reverse('auth_api:users-detail', args=(request.user.id,)):
            return True

        # WORKAROUND: for some reason has_object_permission isn't called for DELETE
        # if view.action == 'destroy':
        #     return view.kwargs['pk'] == request.user.id

        return False

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
