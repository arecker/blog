from django.contrib import admin
from django import forms

from models import Subscriber, Email


class SubscriberAdminForm(forms.ModelForm):
    email_on_save = forms.BooleanField(required=False)

    def save(self, commit=True):
        email_on_save = self.cleaned_data.get('email_on_save', None)
        if email_on_save and not self.instance.is_verified:
            self.instance.send_verify_email()
        return super(SubscriberAdminForm, self).save(commit=commit)

    class Meta:
        model = Subscriber
        exclude = ()



class SubscriberAdmin(admin.ModelAdmin):
    model = Subscriber
    form = SubscriberAdminForm
    readonly_fields = ('verified', 'unsubscribed')
    list_display = ('email', 'subscribed', 'is_active', 'is_verified')
    exclude = ()


class EmailAdminForm(forms.ModelForm):
    send_on_save = forms.BooleanField(required=False)

    def save(self, commit=True):
        send_on_save = self.cleaned_data.get('send_on_save', None)
        if send_on_save and not self.instance.is_sent:
            self.instance.send()
        return super(EmailAdminForm, self).save(commit=commit)

    class Meta:
        model = Email
        exclude = ()


class EmailAdmin(admin.ModelAdmin):
    model = Email
    form = EmailAdminForm
    readonly_fields = ('created', 'modified', 'sent')
    list_display = ('subject', 'is_sent', 'sender', 'created')
    exclude = ()

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_sent:
            return self.readonly_fields + ('subject', 'body', 'is_sent', 'sender')
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return not getattr(obj, 'is_sent', False)

admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Email, EmailAdmin)
