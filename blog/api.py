from rest_framework.routers import DefaultRouter

from content.views import (DocumentViewSet,
                           ImageViewSet,
                           FortuneCookieViewSet)
from subscribing.views import SubscriberViewSet


ROUTER = DefaultRouter()
ROUTER.register('documents', DocumentViewSet)
ROUTER.register('images', ImageViewSet)
ROUTER.register('fortune-cookies', FortuneCookieViewSet)
ROUTER.register('subscribers', SubscriberViewSet)
