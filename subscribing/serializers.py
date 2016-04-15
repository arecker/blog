from rest_framework import serializers

from models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('email',
                  'verify_key',
                  'pk',
                  'subscribed',
                  'is_verified')
