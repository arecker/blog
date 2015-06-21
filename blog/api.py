from rest_framework import routers
from blogging.views import PostViewSet
from subscribing.views import SubscriberViewSet
from coding.views import ProjectViewSet


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'subscribers', SubscriberViewSet)
router.register(r'projects', ProjectViewSet)

