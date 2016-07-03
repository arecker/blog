from rest_framework import viewsets
from rest_framework import permissions
from django.http import Http404, HttpResponse
from django.views.generic import TemplateView


from models import Subscriber
from serializers import SubscriberSerializer


class SubscriberPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        return view.action == 'create'


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = (SubscriberPermissions, )


def verify(request, key):
    try:
        target = Subscriber.objects.get(verify_key=key)
    except Subscriber.DoesNotExist:
        raise Http404

    target.verify()
    return HttpResponse('You have been verified')


def unsubscribe(request, key):
    try:
        target = Subscriber.objects.get(unsubscribe_key=key)
    except Subscriber.DoesNotExist:
        raise Http404

    target.unsubscribe()
    return HttpResponse('You have been unsubscribed')


class NewSubscriberView(TemplateView):
    template_name = 'subscribe.html'
