from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import Subscriber
from serializers import SubscriberSerializer


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

    # Create and Save
    data = JSONParser().parse(request)
    serializer = SubscriberSerializer(data=data)

    if not serializer.is_valid():
        return JSONResponse(serializer.errors, status=400)

    # Check if email is already there
    email = data["email"]
    if not len(Subscriber.objects.filter(email=email)) is 0:
        return HttpResponse(status=400)

    serializer.save()
    return HttpResponse(status=201)


@csrf_exempt
def subscriber_remove(request):
    """
    Remove subscriber
    """
    # Ensure Right Request Type
    if request.method != 'GET':
        return HttpResponse(status=404)

    # Retrieve Subscriber key
    unsubscribe_key = request.GET.get("unsubscribe")
    if not unsubscribe_key:
        return HttpResponse(status=400)

    # Delete Record
    try:
        delete_me = Subscriber.objects.get(unsubscribe_key=unsubscribe_key)
        delete_me.delete()
        return HttpResponse("Alrighty. You are all done with these emails.", status=201)
    except:
        return HttpResponse(status=500)
