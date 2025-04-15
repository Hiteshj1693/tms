from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPollCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.created_by == request.user
