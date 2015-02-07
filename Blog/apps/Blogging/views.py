from django.shortcuts import render_to_response
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