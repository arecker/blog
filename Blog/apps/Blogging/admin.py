from django.contrib import admin
from django import forms
from models import Post
from epiceditor.widgets import AdminEpicEditorWidget


class PostModelForm(forms.ModelForm):
    body = forms.CharField(widget=AdminEpicEditorWidget(themes={'editor':'epic-light.css'}))

    class Meta:
        model = Post
        exclude = ['slug']
        fields = ['title', 'date', 'description', 'published', 'body']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'get_truncated_description', 'published')
    list_filter = ('published',)
    search_fields = ('title', 'description')
    form = PostModelForm


admin.site.register(Post, PostAdmin)
