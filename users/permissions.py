from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            from .models import CustomUser
            CustomUser.objects\
                .filter(id=request.user.id)\
                .update(is_online=timezone.now())
            return True

        return False


class IsAuthenticatedOrReadCustom(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated:
            from users.models import CustomUser
            CustomUser.objects\
                .filter(id=request.user.id)\
                .update(is_online=timezone.now())
            return True

        return False
