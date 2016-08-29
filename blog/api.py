from rest_framework.routers import DefaultRouter

from subscribing.views import SubscriberViewSet


ROUTER = DefaultRouter()
ROUTER.register('subscribers', SubscriberViewSet)
