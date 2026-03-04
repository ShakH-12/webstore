from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view, obj):
    	return obj.user == request.user
    
