from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext

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
        RequestContext(request, {
            'posts': posts,
            'image': image
        })
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

    def get_context_data(self, **kwargs):
        '''
        only display previews if the user is authenticated
        '''
        context = super(PostDetailView, self).get_context_data(**kwargs)
        published = context['post'].published
        authenticated = self.request.user.is_authenticated()

        if not published and not authenticated:
            raise Post.DoesNotExist

        return context
