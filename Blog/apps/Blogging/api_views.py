from django.shortcuts import HttpResponse
from serializers import PostArchiveSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from models import Post


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    TODO: this is defined twice
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def get_posts(request):
    if request.method == 'POST':
        return HttpResponse(status=404)

    # Create and Save
    data = Post.objects.all_archives()
    serializer = PostArchiveSerializer(data, many=True)
    return JSONResponse(data=serializer.data)