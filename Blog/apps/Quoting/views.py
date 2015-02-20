from django.shortcuts import render_to_response, HttpResponse
from models import Post
from feed import RSSFeed


class Data:
    pass


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