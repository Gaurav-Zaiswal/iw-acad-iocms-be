from rest_framework.permissions import BasePermission


class IsStudentUser(BasePermission):
    """
    checks whether or not user is student
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student


class IsTeacherUser(BasePermission):
    """
    checks whether or not user is teacher
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher
