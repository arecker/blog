from django.contrib import admin
from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin)


admin.site.register(Subscriber)
