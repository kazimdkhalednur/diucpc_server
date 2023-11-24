from rest_framework.permissions import BasePermission



class IsGeneralMember(BasePermission):
    """
    Allows access only to General memebers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "general")


class IsAssociativeMember(BasePermission):
    """
    Allows access only to Associative memebers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "associative")


class IsExecutiveMember(BasePermission):
    """
    Allows access only to Executive memebers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "executive")


class IsCoreMember(BasePermission):
    """
    Allows access only to Core memebers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "core")