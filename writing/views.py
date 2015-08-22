from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response, HttpResponse

from viewing.models import Photo
from .models import Post
from .feed import RSSFeed


def index(request):
    posts = Post.objects.published()[:3]
    photo = Photo.objects.enabled().random()

    if photo:
        image = photo.image.url
    else:
        image = None

    return render_to_response(
        'writing/home.html',
        context={
            'posts': posts,
            'image': image
        }
    )


def feed(request):
    stream = RSSFeed()
    return HttpResponse(stream.write(), content_type='application/xml')


class PostListView(ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.published()


class PostDetailView(DetailView):
    model = Post
