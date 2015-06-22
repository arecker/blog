from django.shortcuts import render_to_response, get_object_or_404, HttpResponse
from .models import Post
from .serializers import PostSerializer, PostDetailSerializer
from .feed import RSSFeed
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


def view_post(request, slug):
    return render_to_response('blogging/post.html', {
        'post': get_object_or_404(Post, slug=slug)
    })


def view_post_feed(request):
    feed = RSSFeed()
    return HttpResponse(feed.write(), content_type='application/xml')


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.published()
    permission_classes = (AllowAny,)

    
    def get_queryset(self):
        latest = self.request.query_params.get('latest', None)
        if latest:
            return Post.objects.latest_published()
        return Post.objects.published()


    def get_serializer_class(self):
        if self.action == 'list':
            return PostSerializer
        else:
            return PostDetailSerializer
