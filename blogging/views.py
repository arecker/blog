from django.shortcuts import render_to_response, get_object_or_404, HttpResponse
from .models import Post
from .serializers import PostSerializer
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
    queryset = Post.objects.filter(published=True)
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Post.objects.filter(published=True)
        latest = self.request.query_params.get('latest', None)
        if latest:
            if queryset.count() > 0:
                queryset = [queryset[0],]
            else:
                queryset = []
        return queryset
