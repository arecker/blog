from rest_framework import routers
from blogging.views import PostViewSet


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
