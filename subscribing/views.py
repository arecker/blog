from rest_framework import viewsets
from rest_framework.response import Response
from .models import Subscriber
from .serializers import SubscriberSerializer


class SubscriberViewSet(viewsets.ViewSet):
    queryset = Subscriber.objects.all()


    def list(self, request):
        queryset = Subscriber.objects.all()
        serializer = SubscriberSerializer(queryset, many=True)
        return Response(serializer.data)