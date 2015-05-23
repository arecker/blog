from django.shortcuts import render_to_response, get_object_or_404
from .models import Post
from .serializers import PostSerializer
from rest_framework import viewsets


def view_post(request, slug):
    return render_to_response('blogging/post.html', {
        'post': get_object_or_404(Post, slug=slug)
    })


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer