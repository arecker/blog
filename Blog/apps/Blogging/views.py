from django.shortcuts import render_to_response, HttpResponse
from django.utils import feedgenerator
from models import Post


class Data:
    pass


def get_home(request):
    data = Data()
    data.posts = Post.objects.all_archives()
    data.latest = Post.objects.latest()
    return render_to_response("blogging/home.html", { "data": data })


def get_post(request, slug):
    post = Post.objects.get(slug=slug)
    return render_to_response('blogging/post.html', { 'data': post })


def get_feed(request):
    feed = feedgenerator.Rss201rev2Feed(
        title='Blog by Alex Recker',
        link='http://alexrecker.com',
        description='Hey - my name is Alex Recker.  I like to write words.',
        language=u'en',
    )

    for post in Post.objects.all_feed_items():
        feed.add_item(
            title=post['title'],
            description=post['description'],
            link='http://alexrecker.com/' + post['slug'] + '/'
        )

    str = feed.writeString('utf-8')
    return HttpResponse(str)