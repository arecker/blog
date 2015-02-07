from django.shortcuts import render_to_response
from models import Post


class Data:
    pass


def get_home(request):
    data = Data()
    posts = Post.objects.all().order_by('-date')
    data.latest = posts[0]
    data.posts = posts
    return render_to_response("blogging/home.html", { "data": data })