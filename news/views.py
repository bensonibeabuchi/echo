from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from news_api.models import *
from .filters import ArticleFilter
from django.core.paginator import Paginator
import requests
from django.template.defaultfilters import slugify


API_KEY = '981b08fa899d4d44b490545678025616'
API_KEY2 = '55723df2ad2b4324a023948ca4035031'


def index(request):
    country = request.GET.get('country')
    category = request.GET.get('category')
    q = request.GET.get('q')

    if country:
        url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
    elif category:
        url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}'
    elif q:
        url = f'https://newsapi.org/v2/everything?q={q}&apiKey={API_KEY}'
    else:
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])

    paginator = Paginator(articles, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'articles': page_obj
    }

    return render(request, 'news/index.html', context)


@login_required(login_url='login')
def apiview(request):
    articles_per_page = 10

    # Get the filter parameters from the request's GET parameters
    myFilter = ArticleFilter(request.GET, queryset=Article.objects.all())
    db_articles = myFilter.qs  # we now Apply the filter to the queryset

    # Now Create a Paginator instance based on the filtered queryset
    paginator = Paginator(db_articles, articles_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    context = {
        'db_articles': page,
        'myFilter': myFilter,
        'page': page,
    }
    return render(request, 'news/apiview.html', context)


def single_dbNews(request, slug):
    myFilter = ArticleFilter(request.GET, queryset=Article.objects.all())

    single_article = get_object_or_404(Article, slug=slug)
    context = {
        'single_article': single_article,
        'myFilter': myFilter,
    }
    return render(request, 'news/single_dbNews.html', context)


def single_news(request, slug):

    country = request.GET.get('country')
    category = request.GET.get('category')
    q = request.GET.get('q')

    if country:
        url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
    elif category:
        url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}'
    elif q:
        url = f'https://newsapi.org/v2/everything?q={q}&apiKey={API_KEY}'
    else:
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])

    slugs = []  # Create a list to store slugs for each article
    for article in articles:
        title = article.get('title', 'No title available')
        print(title)
        slug = slugify(title)
        slugs.append(slug)

    # Use the index of the requested slug to find the corresponding article
    try:
        index = slugs.index(slug)
        single_article = articles[index]
    except ValueError:
        raise Http404("Article not found")

    single_article = articles.objects.get(slug=slug)
    context = {
        'single_article': single_article,
        'slug': slug,
    }

    return render(request, 'news/single_dbNews.html', context)
