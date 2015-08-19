from django.views.generic.detail import DetailView
from .models import Post


class PostDetailView(DetailView):
    model = Post
