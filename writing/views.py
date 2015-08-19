from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post


class PostListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.published()


class PostDetailView(DetailView):
    model = Post
