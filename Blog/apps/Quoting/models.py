from django.db import models
import datetime


class Quote(models.Model):
    text = models.TextField(verbose_name='Text')
    author = models.CharField(verbose_name='Author', max_length=120)
    author_description = models.CharField(verbose_name='Author Description', max_length=240, blank=True, null=True)
    submitter = models.CharField(verbose_name="Submitter", max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(verbose_name='Time Stamp', db_index=True, default=datetime.datetime.now(), blank=True)
    approved = models.BooleanField(verbose_name="Approved", default=False)


    def get_truncated_text(self, length=50, suffix='...'):
        if not self.text:
            return ''
        if len(self.text) <= length:
            return self.text
        else:
            return ' '.join(self.text[:length+1].split(' ')[0:-1]) + suffix
    get_truncated_text.short_description = "Text"