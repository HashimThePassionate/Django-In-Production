from rest_framework import serializers
from . import models

class AuthorSerializer(serializers.ModelSerializer):
    long_bio = serializers.CharField(source='bio')  # Rename bio to long_bio
    short_bio = serializers.CharField(source='fetch_short_bio')  # Access model method

    class Meta:
        model = models.Author
        fields = ['id', 'name', 'email', 'long_bio', 'short_bio']