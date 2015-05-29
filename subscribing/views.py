from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAdminUser
from .models import Subscriber
from .serializers import SubscriberSerializer


class SubscriberEndpointPermission(BasePermission):
    """
    The app should allow users to be created and destroyed,
    but listing is restricted to admins only
    """
    def has_permission(self, request, view):
        open_methods = ['create', 'destroy']
        if view.action in open_methods:
            return True
        return IsAdminUser().has_permission(request, view)


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [SubscriberEndpointPermission,]
