from rest_framework import permissions

class IsTripOrganizerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the trip organizer
        return obj.trip_organizer == request.user


class IsAdminOrTripParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff or
            request.user == obj.trip_organizer or
            request.user in obj.participants.all()
        )
    
