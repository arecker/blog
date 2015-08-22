from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response
from .models import Post


def index(request):
    posts = Post.objects.published()[:3]
    return render_to_response(
        'writing/home.html',
        context={'posts': posts}
    )


class PostListView(ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.published()


class PostDetailView(DetailView):
    model = Post
