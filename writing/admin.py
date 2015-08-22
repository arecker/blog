from django.contrib import admin

from .models import Post
from .forms import PostModelForm
from subscribing.models import Subscriber


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'published')
    list_filter = ('published',)
    search_fields = ('title', 'description')
    ordering = ['-date']
    prepopulated_fields = {'slug': ['title']}
    form = PostModelForm

    def email_post(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(
                request,
                """You probably don\'t want to send
                out that many emails."""
            )
        else:
            post = queryset.first()
            people = Subscriber.objects.verified()
            for person in people:
                person.send_post(post)
            self.message_user(
                request,
                'Post {0} sent to {1} people'.format(
                    post.title, len(people)
                )
            )
    actions = ['email_post']

admin.site.register(Post, PostAdmin)
