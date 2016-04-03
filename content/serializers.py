from rest_framework import serializers

from models import Document, Image, FortuneCookie


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'slug', 'file')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'slug', 'file')


class FortuneCookieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FortuneCookie
        fields = ('id', 'name', 'slug', 'text')
