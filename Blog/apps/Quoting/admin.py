from django.contrib import admin
from models import Quote


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('get_truncated_text', 'author', 'author_description', 'submitter', 'timestamp', 'approved')
    list_filter = ('approved',)
    search_fields = ('author', 'author_description')
    ordering = ['timestamp']


admin.site.register(Quote, QuoteAdmin)
