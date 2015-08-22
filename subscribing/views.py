from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from .models import Subscriber
from .forms import SubscriberForm


def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('subscribe-thanks'))
    else:
        form = SubscriberForm()
    return render_to_response(
        'subscribing/subscribe.html',
        RequestContext(request, {'form': form})
    )


def verify(self, key=None):
    subscriber = Subscriber.objects.get(pk=key)
    subscriber.verify()
    return render_to_response('subscribing/verified.html', {})
