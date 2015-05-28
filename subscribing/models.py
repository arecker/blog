from django.db import models
import uuid


class Subscriber(models.Model):
    email = models.EmailField()
    full_text = models.BooleanField(default=False)
    key = models.UUIDField(primary_key=True, default=uuid.uuid4)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return self.email
