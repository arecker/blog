from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from content.models import Document, Image, FortuneCookie

BASE_READONLY_FIELDS = ('created', 'edited')
PREPOPULATED_FIELDS = {'slug': ['name']}

class DocumentAdmin(admin.ModelAdmin):
    model = Document
    readonly_fields = BASE_READONLY_FIELDS
    prepopulated_fields = PREPOPULATED_FIELDS
    list_display = ('name', 'slug', 'filename')
    exclude = ()


class ImageAdmin(AdminImageMixin, admin.ModelAdmin):
    model = Image
    readonly_fields = BASE_READONLY_FIELDS
    prepopulated_fields = PREPOPULATED_FIELDS
    list_display = ('name', 'slug', 'thumbnail')
    exclude = ()


class FortuneCookieAdmin(admin.ModelAdmin):
    model = FortuneCookie
    readonly_fields = BASE_READONLY_FIELDS
    prepopulated_fields = PREPOPULATED_FIELDS
    list_display = ('name', 'slug', 'truncated_text')


admin.site.register(Document, DocumentAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(FortuneCookie, FortuneCookieAdmin)
