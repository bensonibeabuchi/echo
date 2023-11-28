from django.urls import path
from .views import *
ReporterNewsListView


urlpatterns = [
    path('', ArticleHomepage.as_view(), name='articles'),
    path('get_articles/', get_article, name='get_articles'),
    path('add_article/', AddArticles.as_view(), name='add_articles'),
    path('add_reporter/', AddReporter.as_view(), name='add_reporter'),
    path('list_reporter/', ListReporters.as_view(), name='list_reporter'),
    path('category/<category>/', ArticleHomepage.as_view(), name='article-list'),
    path('reporter/<str:reporter_name>/',
         ReporterNewsListView.as_view(), name='reporter_news_list'),
    path('<slug:slug>/', ArticleDetailPage.as_view(), name='article_detail'),
]
