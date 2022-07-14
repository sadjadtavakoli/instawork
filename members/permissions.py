from rest_framework.permissions import IsAuthenticated


class DeleteMemberPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.user.is_admin
        return False
