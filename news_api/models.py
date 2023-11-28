from django.db import models
from django.utils.text import slugify
from users.models import CustomUser
import uuid


class Article(models.Model):
    class ArticleStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    class ArticleCategory(models.TextChoices):
        GENERAL = 'general', 'General'
        BUSINESS = 'business', 'Business'
        ENTERTAINMENT = 'entertainment', 'Entertainment'
        HEALTH = 'health', 'Health'
        SCIENCE = 'science', 'Science'
        SPORTS = 'sports', 'Sports'
        TECHNOLOGY = 'technology', 'Technology'

    id = models.UUIDField(max_length=36, unique=True, primary_key=True, default=uuid.uuid4, editable=False)  # noqa
    title = models.CharField(blank=True, null=True, max_length=500)  # noqa
    content = models.TextField(blank=True, null=True)  # noqa
    image = models.ImageField(upload_to="images/", max_length=1000, blank=True, null=True)  # noqa
    category = models.CharField(choices=ArticleCategory.choices, max_length=255, default=ArticleCategory.ENTERTAINMENT)  # noqa
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1, null=True)  # noqa
    author = models.CharField(blank=True, max_length=255, null=True, default="unknown")  # noqa
    excerpt = models.TextField(blank=True, default='Default excerpt', null=True)  # noqa
    timestamp = models.DateTimeField(auto_now_add=True, null=True)  # noqa
    slug = models.SlugField(max_length=1000)  # noqa
    status = models.CharField(max_length=10, choices=ArticleStatus.choices, default=ArticleStatus.PUBLISHED)  # noqa
    url = models.URLField(max_length=1000, blank=True, null=True)  # noqa
    source = models.CharField(max_length=1000, blank=True, null=True)  # noqa

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
