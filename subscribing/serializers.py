from rest_framework import serializers

from models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    def create(self, *args):
        instance = super(SubscriberSerializer, self).create(*args)
        instance.send_verify_email()
        return instance

    class Meta:
        model = Subscriber
        fields = ('email',
                  'verify_key',
                  'pk',
                  'subscribed',
                  'is_verified')
