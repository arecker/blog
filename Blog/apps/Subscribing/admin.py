from django.contrib import admin
from django import forms
from models import Subscriber


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


admin.site.register(Subscriber, SubscriberAdmin)
