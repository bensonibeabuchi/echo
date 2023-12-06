from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('apiview/', apiview, name='apiview'),
    path('<int:pk>/', single_news, name='single_newsO'),
    path('<slug:slug>/', single_dbNews, name='single_news'),
]
