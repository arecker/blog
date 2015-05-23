from django.contrib import admin
from django import forms
from epiceditor.widgets import AdminEpicEditorWidget
from . import models


class PostModelForm(forms.ModelForm):
    body = forms.CharField(widget=AdminEpicEditorWidget(themes={'editor':'epic-light.css'}))

    class Meta:
        model = models.Post
        fields = ['title', 'slug', 'date', 'published', 'description', 'image_url', 'body']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'published')
    list_filter = ('published',)
    search_fields = ('title', 'description')
    ordering = ['-date']
    form = PostModelForm


admin.site.register(models.Post, PostAdmin)