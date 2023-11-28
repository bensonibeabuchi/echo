from requests import request
from rest_framework import serializers
from .models import Article
from django.urls import reverse  # Import reverse here


class ArticleSerializer(serializers.ModelSerializer):
    reporter_username = serializers.CharField(
        source='reporter.username', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'image', 'category', 'reporter', 'reporter_username',
                  'author', 'excerpt', 'timestamp', 'slug', 'status', 'url', 'source']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['reporter_username'] = instance.reporter.username
    #     return data
