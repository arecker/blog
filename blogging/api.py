from rest_framework import routers
import blogging, subscribing


router = routers.DefaultRouter()
router.register(r'posts', blogging.views.PostViewSet)