from django.contrib import admin

from .models import Author, Post
from .forms import PostModelForm


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'published')
    list_filter = ('published',)
    search_fields = ('title', 'description')
    ordering = ['-date']
    prepopulated_fields = {'slug': ['title']}

    form = PostModelForm


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
