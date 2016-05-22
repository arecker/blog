from rest_framework import serializers

from models import FortuneCookie


class FortuneCookieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FortuneCookie
        fields = ('id', 'name', 'slug', 'text')
