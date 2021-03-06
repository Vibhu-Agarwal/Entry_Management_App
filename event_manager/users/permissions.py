from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.mixins import UserPassesTestMixin


class IsHostMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_host


class IsManagementMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 'management'


class IsNotManagementMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type != 'management'


class LoggedOutRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated


class IsHostOrLoggedOutMixin(UserPassesTestMixin):
    def test_func(self):
        return (not self.request.user.is_authenticated) or self.request.user.is_host


class IsVisitHost(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return obj.host.is_host and (obj.host == request.user)

        return obj.host.is_host and (obj.host == request.user)


class IsVisitVisitor(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return (obj.host.user_type == 'visitor') and (obj.visitor == request.user)

        return (obj.host.user_type == 'visitor') and (obj.visitor == request.user)
