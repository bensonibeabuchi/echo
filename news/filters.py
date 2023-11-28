import django_filters
from news_api.models import *
from django_filters.rest_framework import FilterSet
from news_api.models import Article


class ArticleFilter(django_filters.FilterSet):
    source = django_filters.CharFilter(
        field_name='source', lookup_expr='icontains')
    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ('category', 'reporter')


class ArticleFilterAPI(django_filters.FilterSet):
    reporterName = django_filters.CharFilter(
        field_name='reporter__username', lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ('category', 'reporter')
