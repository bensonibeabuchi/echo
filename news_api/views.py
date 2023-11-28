import uuid
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from news_api.permissions import IsReporterOrReadOnly
from news.filters import ArticleFilterAPI
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Article
from .serializers import ArticleSerializer
from users.serializers import *
from drf_spectacular.utils import extend_schema
from users.models import CustomUser
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


API_KEY = '981b08fa899d4d44b490545678025616'
API_KEY2 = '55723df2ad2b4324a023948ca4035031'


@extend_schema(responses=ArticleSerializer)
@api_view(["GET"])
def get_article(request):
    """
    A request to update the articles on the database from sources all over the world automatically
    """

    url = f'https://newsapi.org/v2/top-headlines?country=us&category=ENTERTAINMENT&apiKey={API_KEY}'
    headers = {'X-Api-Key': API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        all_articles = response.json()
        converted_articles = dict(all_articles)

        for news in converted_articles["articles"]:

            fetched_title = news.get("title", "unknown")
            fetched_url = news.get("url", "unknown")
            fetched_excerpt = news.get("description", "unknown")
            fetched_image = news.get("urlToImage", "")
            fetched_timestamp = news.get("publishedAt", "unknown")
            fetched_content = news.get("content", "unknown")
            fetched_author = news.get("author", "unknown",)
            fetched_source = news["source"].get("name", "unknown")

            # Check if the article already exists in the database by title
            existing_article = Article.objects.filter(
                title=fetched_title).first()

            if not existing_article:
                # Article doesn't exist in the database, create it
                id = uuid.uuid4()
                Article.objects.create(id=id,
                                       title=fetched_title,
                                       url=fetched_url,
                                       source=fetched_source,
                                       author=fetched_author,
                                       excerpt=fetched_excerpt,
                                       timestamp=fetched_timestamp,
                                       content=fetched_content,
                                       image=fetched_image)

        all_db_articles = Article.objects.all()
        seriealized_articles = ArticleSerializer(all_db_articles, many=True)
        return Response(seriealized_articles.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "failed to fetch article"}, status=status.HTTP_400_BAD_REQUEST)


class ArticleHomepage(generics.ListAPIView):
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = Article.objects.filter(status='published')
    filterset_class = ArticleFilterAPI
    search_fields = ['title', 'content', 'source']
    ordering_fields = ['timestamp']
    permission_classes = [IsReporterOrReadOnly]

    """
    A request to get ALL articles from the database.
    """

    @swagger_auto_schema(operation_summary="This endpoint is responsible for listing all the news in the database", operation_description="These are the list of all the news")
    def get(self, request, category=None):

        queryset = self.filter_queryset(self.get_queryset())
        serialized_articles = ArticleSerializer(queryset, many=True)

        # if category:
        #     all_articles = Article.objects.filter(
        #         status='published', category=category)
        #     serialized_articles = ArticleSerializer(all_articles, many=True)
        #     return Response(serialized_articles.data, status=status.HTTP_200_OK)
        # else:
        #     all_articles = Article.objects.filter(status='published')
        #     serialized_articles = ArticleSerializer(all_articles, many=True)

        return Response(serialized_articles.data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(operation_summary="This endpoint is responsible for POSTING news articles into the database", operation_description="New Article Posting into the database")
    # def post(self, request):
    #     new_article = ArticleSerializer(data=request.data)
    #     if new_article.is_valid():
    #         new_article.save()
    #         message = {"Success": "Article has been added successfully"}
    #         return Response(message, status=status.HTTP_201_CREATED)
    #     return Response(new_article.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailPage(APIView):
    """
    A request to get a single article from the database.
    """
    serializer_class = ArticleSerializer
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsReporterOrReadOnly]

    @swagger_auto_schema(operation_summary="This endpoint is responsible for RETRIEVING a single news article from the database", operation_description="This is just one news article")
    def get(self, request, slug):
        single_article = get_object_or_404(Article, slug=slug)
        serialized_single = ArticleSerializer(single_article)
        return Response(serialized_single.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="This endpoint is responsible for MODIFYING a single news article from the database", operation_description="This is just one news article")
    def put(self, request, slug):
        try:
            single_article = get_object_or_404(Article, slug=slug)
        except Article.DoesNotExist:
            return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

        change_article = ArticleSerializer(
            single_article, data=request.data, partial=True)
        if change_article.is_valid():
            change_article.save()
            message = {"Success": "Article has been updated successfully"}
            return Response(message, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(change_article.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="This endpoint is responsible for DELETING a single news article from the database", operation_description="This is just one news article")
    def delete(self, request, slug):
        single_article = get_object_or_404(Article, slug=slug)

        if request.user != single_article.reporter:
            print(request.user)
            message = {'status': "You are not allowed to delete this article"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)

        single_article.delete()
        message = {"Success": "Article is deleted successfully"}
        return Response(message, status=status.HTTP_204_NO_CONTENT)

  # single_article = Article.objects.get(slug=slug)

        # if single_article:
        #     single_article.delete()
        #     message = {
        #         "Success": "Article is deleted successfully"}
        #     return Response(message, status=status.HTTP_204_NO_CONTENT)
        # else:
        #     return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)


class ReporterNewsListView(APIView):
    """
    A view to list all news articles associated with a reporter.
    """
    @swagger_auto_schema(operation_summary="This endpoint is responsible for RETRIEVING all the news article associated with a reporter by using their username as a parameter", operation_description="This is just one news article")
    def get(self, request, reporter_name):
        try:
            reporter = CustomUser.objects.get(username=reporter_name)
        except CustomUser.DoesNotExist:
            return Response({"error": "Reporter not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all news articles associated with the reporter
        all_articles = Article.objects.filter(reporter=reporter)

        # Serialize the news articles
        serializer = ArticleSerializer(all_articles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AddArticles(APIView):

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    """
    A view to add new articles manually.
    """
    @swagger_auto_schema(operation_summary="This endpoint is responsible for ADDING a news article manually to the database", operation_description="This is just to add new Articles MANUALLY to the database")
    def post(self, request):
        new_article = ArticleSerializer(data=request.data)
        if new_article.is_valid():
            new_article.save()

            message = {
                "Success": 'Article has been added successfully'}
            return Response(message, status=status.HTTP_201_CREATED)
        return Response(new_article.errors, status=status.HTTP_400_BAD_REQUEST)


class AddReporter(generics.CreateAPIView):

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    """
    A view to add new Reporters to the database.
    """
    @swagger_auto_schema(operation_summary="This endpoint is responsible to add new Reporters to the database", operation_description="This is just to add new Reporters to the database")
    def post(self, request):
        new_reporter = CustomUserSerializer(data=request.data)
        if new_reporter.is_valid():
            new_reporter.save()

            message = {
                "Success": 'Reporter has been added successfully'}
            return Response(message, status=status.HTTP_201_CREATED)
        return Response(new_reporter.errors, status=status.HTTP_400_BAD_REQUEST)


class ListReporters(generics.ListAPIView):

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
