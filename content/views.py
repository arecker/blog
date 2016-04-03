from rest_framework import viewsets, decorators
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from content.models import Document, Image, FortuneCookie
from serializers import (DocumentSerializer,
                         ImageSerializer,
                         FortuneCookieSerializer)


class BaseViewSetMixin(object):
    @decorators.list_route(methods=['get'], url_path='random')
    def random(self, request):
        item = self.get_queryset().pluck()
        if not item:
            raise NotFound
        serialzed_item = self.get_serializer(item)
        return Response(serialzed_item.data)

    @decorators.list_route(methods=['get'])
    def slug(self, request):
        query = request.query_params.get('q', None)
        try:
            item =  self.get_queryset().slug(slug=query)
            serialzed_item = self.get_serializer(item)
            return Response(serialzed_item.data)
        except self.queryset.model.DoesNotExist:
            raise NotFound


class DocumentViewSet(BaseViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class ImageViewSet(BaseViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class FortuneCookieViewSet(BaseViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = FortuneCookie.objects.all()
    serializer_class = FortuneCookieSerializer
