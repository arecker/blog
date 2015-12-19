from django.contrib import admin
from post_office.admin import Email, Log, EmailTemplate
from .models import Subscriber, Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    def send_email(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(
                request,
                """You probably don\'t want to send
                out that many emails."""
            )
        else:
            letter = queryset.first()
            people = Subscriber.objects.verified()
            letter.send(people)
            self.message_user(
                request,
                'Newsletter {0} sent to {1} people'.format(
                    letter.subject, len(people)
                )
            )
    actions = ['send_email']


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'verified')
    list_filter = ('verified',)
    search_fields = ('email', )
    ordering = ['timestamp']


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.unregister(Email)
admin.site.unregister(Log)
admin.site.unregister(EmailTemplate)
