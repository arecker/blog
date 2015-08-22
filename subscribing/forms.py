from django.forms import ModelForm

from .models import Subscriber


class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
