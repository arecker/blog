from django.shortcuts import HttpResponse
from .models import Post
from .serializers import PostSerializer, PostDetailSerializer
from .feed import RSSFeed
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.views.generic.detail import DetailView


class PostDetailView(DetailView):
    model = Post


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
