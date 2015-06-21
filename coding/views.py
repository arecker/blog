from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import ProjectSerializer
from .models import Project


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = (AllowAny,)

