from django.http import Http404, HttpResponse
from rest_framework import viewsets
from sorl.thumbnail import get_thumbnail

from content.models import FortuneCookie, Image
from serializers import FortuneCookieSerializer


class FortuneCookieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FortuneCookie.objects.all()
    serializer_class = FortuneCookieSerializer


def random_image(request):
    image = Image.objects.pluck()

    if not image:
        raise Http404('No images uploaded')

    file = get_thumbnail(image.file, '500')

    return HttpResponse(file.read(), content_type='image/png')
