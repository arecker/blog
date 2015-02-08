from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import Subscriber
from serializers import SubscriberSerializer
try:
    from Blog.settings.production import API_KEY
except ImportError:
    from Blog.settings.development import API_KEY


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def subscriber_add(request):
    """
    Add subscriber
    """
    # Ensure Right Request Type
    if request.method != 'POST':
        return HttpResponse(status=404)

    # Validate App Key
    if API_KEY != request.GET.get("key"):
        return HttpResponse(status=403)

    # Create and Save
    data = JSONParser().parse(request)
    serializer = SubscriberSerializer(data=data)

    # Check if email is already there
    email = data["email"]
    if not len(Subscriber.objects.filter(email=email)) is 0:
        return HttpResponse(status=400)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse(status=201)
    return JSONResponse(serializer.errors, status=400)