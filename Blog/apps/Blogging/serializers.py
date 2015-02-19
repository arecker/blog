from rest_framework import serializers
from models import Post


class PostArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'description', 'image_url', 'date')