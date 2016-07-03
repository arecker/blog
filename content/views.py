from rest_framework import viewsets, decorators
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.http import HttpResponse, Http404

from content.models import FortuneCookie, Image
from serializers import FortuneCookieSerializer


class FortuneCookieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FortuneCookie.objects.all()
    serializer_class = FortuneCookieSerializer


def random_image(request):
    image = Image.objects.pluck()

    if not image:
        raise Http404('No images uploaded')

    with open(image.file.path) as file:
        return HttpResponse(file.read(), content_type='image/png')
