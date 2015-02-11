from django.contrib import admin
from django import forms
from models import Subscriber, Newsletter


class SubscriberModelForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        exclude = ['unsubscribe_key']
        fields = ['email', 'full_text']


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribe_date', 'full_text')
    list_filter = ('full_text',)
    search_fields = ('email',)
    ordering = ['-subscribe_date']
    form = SubscriberModelForm


class NewsletterModelForm(forms.ModelForm):
    class Meta:
        model = Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'post']


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Newsletter, NewsletterAdmin)