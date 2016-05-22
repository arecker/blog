from rest_framework import viewsets, decorators
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.http import HttpResponse, Http404

from content.models import FortuneCookie, Image
from serializers import FortuneCookieSerializer


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


class FortuneCookieViewSet(BaseViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = FortuneCookie.objects.all()
    serializer_class = FortuneCookieSerializer


def random_image(request):
    try:
        image = Image.objects.pluck()
    except Image.DoesNotExist:
        return Http404()

    with open(image.file.path) as file:
        return HttpResponse(file.read(), content_type='image/png')
