from django.shortcuts import render_to_response, get_object_or_404
from .models import Post
from .serializers import PostSerializer
from rest_framework import viewsets


def view_post(request, slug):
    return render_to_response('blogging/post.html', {
        'post': get_object_or_404(Post, slug=slug)
    })


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published=True)

    def get_queryset(self):
        queryset = Post.objects.filter(published=True)
        latest = self.request.query_params.get('latest', None)
        if latest:
            queryset = [queryset[0],]
        return queryset
