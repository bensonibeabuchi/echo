# Generated by Django 4.2.7 on 2024-04-12 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_api', '0003_alter_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(blank=True, default='unknown', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('general', 'General'), ('business', 'Business'), ('entertainment', 'Entertainment'), ('health', 'Health'), ('science', 'Science'), ('sports', 'Sports'), ('technology', 'Technology')], default='business', max_length=255),
        ),
    ]
