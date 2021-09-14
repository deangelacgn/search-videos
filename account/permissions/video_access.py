from rest_framework import permissions


class VideoAccessPermision(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        elif request.method == 'PATCH':
            return request.user.is_authenticated
        elif request.method == 'DELETE':
            return request.user.is_authenticated or request.user.is_admin
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated():
            return False

        if request.method == 'PATCH':
            return obj.user == request.user
        elif request.method == 'DELETE':
            return obj.user == request.user or request.user.is_superuser
        else:
            return False