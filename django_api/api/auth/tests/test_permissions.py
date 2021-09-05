from unittest.mock import MagicMock

from django.test import TestCase
from django.urls import reverse

from django_api.api.auth.permissions import IsCreateView, IsStaff, IsOwnUserProfile


class PermissionsTests(TestCase):
    """
    Test custom permission classes
    """

    def assert_is_create_view(self, view_action, expected_access):
        """
        Helper for asserting IsCreateView view-level permissions.
        """
        perm = IsCreateView()
        mock_view = MagicMock()
        mock_view.action = view_action
        access = perm.has_permission(MagicMock(), mock_view)

        self.assertEqual(access, expected_access)

    def test_is_create_view_has_permission_create(self):
        """
        Permission is granted when the view action is "create".
        """
        self.assert_is_create_view('create', True)

    def test_is_create_view_has_permission_not_create(self):
        """
        Permission is denied when the view action is NOT "create".
        """
        view_actions = ['list', 'retrieve', 'update', 'partial_update', 'destroy']
        for a in view_actions:
            self.assert_is_create_view(a, False)

    def test_is_create_view_has_object_permission(self):
        """
        Permission is always denied at the object level.
        """
        perm = IsCreateView()
        access = perm.has_permission(MagicMock(), MagicMock())

        self.assertFalse(access)

    def assert_is_staff(self, is_authenticated, is_staff, expected_access):
        """
        Helper for asserting IsStaff view-level and object-level permissions.
        """
        perm = IsStaff()
        mock_user = MagicMock()
        mock_user.is_authenticated = is_authenticated
        mock_user.is_staff = is_staff
        mock_request = MagicMock()
        mock_request.user = mock_user
        mock_view = MagicMock()
        access = perm.has_permission(mock_request, mock_view)
        object_access = perm.has_object_permission(mock_request, mock_view, MagicMock())

        self.assertEqual(access, object_access)
        self.assertEqual(access, expected_access)

    def test_is_staff_as_staff(self):
        """
        Permission is granted when the user is staff.
        """
        self.assert_is_staff(True, True, True)

    def test_is_staff_as_not_staff(self):
        """
        Permission is denied when the user is NOT staff.
        """
        self.assert_is_staff(True, False, False)

    def test_is_staff_unauthenticated(self):
        """
        Permission is denied when the user is unauthenticated.
        """
        self.assert_is_staff(False, False, False)

    def test_is_staff_unauthenticated_staff(self):
        """
        Permission is denied when the user is unauthenticated but appears to be staff (should be impossible).
        """
        self.assert_is_staff(False, True, False)

    def build_is_own_user_profile_mock_request(self, authenticated, url):
        """
        Helper for building IsOwnUserProfile request.
        NOTE:
            Authenticated:      request.user.id == 1
            Un-authenticated:   request.user.id == None
        """
        mock_user = MagicMock()
        mock_user.is_authenticated = authenticated
        mock_user.id = 1 if authenticated else None

        mock_request = MagicMock()
        mock_request.get_full_path = MagicMock(return_value=url)
        mock_request.user = mock_user

        return mock_request

    def test_is_own_user_profile_has_permission_unauthenticated(self):
        """
        Permission is denied for unauthenticated users at view level.
        """
        perm = IsOwnUserProfile()

        # check unauthenticated with list url
        self.assertFalse(
            perm.has_permission(
                self.build_is_own_user_profile_mock_request(False, reverse('auth_api:users-list')),
                MagicMock()
            )
        )

        # check unauthenticated with detail url
        self.assertFalse(
            perm.has_permission(
                self.build_is_own_user_profile_mock_request(False, reverse('auth_api:users-detail', args=(1,))),
                MagicMock()
            )
        )

    def test_is_own_user_profile_has_permission_authenticated(self):
        """
        Permission is denied for authenticated users accessing list url and granted fro accessing detail url at view
        level.
        """
        perm = IsOwnUserProfile()

        # check authenticated with list url
        self.assertFalse(
            perm.has_permission(
                self.build_is_own_user_profile_mock_request(True, reverse('auth_api:users-list')),
                MagicMock()
            )
        )

        # check authenticated with detail url
        self.assertTrue(
            perm.has_permission(
                self.build_is_own_user_profile_mock_request(True, reverse('auth_api:users-detail', args=(1,))),
                MagicMock()
            )
        )

        # check authenticated with unsupported url
        self.assertFalse(
            perm.has_permission(
                self.build_is_own_user_profile_mock_request(True, '/test-unsupported-url'),
                MagicMock()
            )
        )

    def test_is_own_user_profile_has_object_permission(self):
        """
        Permission is granted only if logged-in user matches user being accessed.
        """
        mock_request_owned = self.build_is_own_user_profile_mock_request(
            True,
            reverse('auth_api:users-detail', args=(1,))
        )
        mock_obj_owned = MagicMock()
        mock_obj_owned.id = 1

        mock_request_not_owned = self.build_is_own_user_profile_mock_request(
            True,
            reverse('auth_api:users-detail', args=(2,))
        )
        mock_obj_not_owned = MagicMock()
        mock_obj_not_owned.id = 2

        perm = IsOwnUserProfile()
        self.assertTrue(perm.has_object_permission(mock_request_owned, MagicMock(), mock_obj_owned))
        self.assertFalse(perm.has_object_permission(mock_request_not_owned, MagicMock(), mock_obj_not_owned))
