from rest_framework.routers import DefaultRouter

from content.views import FortuneCookieViewSet
from subscribing.views import SubscriberViewSet


ROUTER = DefaultRouter()
ROUTER.register('fortune-cookies', FortuneCookieViewSet)
ROUTER.register('subscribers', SubscriberViewSet)
