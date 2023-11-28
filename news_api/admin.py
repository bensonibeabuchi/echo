from django.contrib import admin
from .models import Article

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", 'timestamp', "source", "author",
                    "status", "category", ]
    list_editable = ["status", "category", ]
    list_filter = ["category", "reporter", "source", "author", "status"]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, ArticleAdmin)
