from django.shortcuts import render_to_response, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import Post
from serializers import PostArchiveSerializer
from feed import RSSFeed


class Data:
    pass


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    TODO: this is defined twice
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def get_home(request):
    data = Data()
    data.posts = Post.objects.all_archives()
    data.latest = Post.objects.latest()
    return render_to_response("blogging/home.html", { "data": data })


def get_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        return render_to_response('blogging/post.html', { 'data': post })
    except Post.DoesNotExist:
        return render_to_response('common/404.html')


def get_feed(request):
    feed = RSSFeed()
    return HttpResponse(feed.write(), content_type='application/xml')


@csrf_exempt
def get_archives(request):
    if request.method == 'POST':
        return HttpResponse(status=404)

    # Create and Save
    data = Post.objects.all()
    serializer = PostArchiveSerializer(data, many=True)
    return JSONResponse(data=serializer.data)