from django.contrib import admin
from .models import Author, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'published')
    list_filter = ('published',)
    search_fields = ('title', 'description')
    ordering = ['-date']
    prepopulated_fields = {'slug': ['title']}


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
