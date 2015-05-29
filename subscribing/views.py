from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAdminUser
from django.shortcuts import get_object_or_404, render_to_response
from .models import Subscriber
from .serializers import SubscriberSerializer


def get_unsubscribe_view(request, key=None):
    return render_to_response('subscribing/unsubscribe.html', {
        'key': get_object_or_404(Subscriber, key=key).key
    })


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
