from django.contrib import admin
from models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'get_truncated_description', 'published')
    list_filter = ('published',)
    search_fields = ('title', 'description')


admin.site.register(Post, PostAdmin)
