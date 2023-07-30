from django.db import models


class NewsModel(models.Model):
    article_title = models.CharField(blank=False, null=False, max_length=30)
    article_content = models.TextField(blank=False, null=False)
    article_author = models.CharField(blank=False, null=False, max_length=30)
    article_author_key = models.BigIntegerField(blank=False, null=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


class CompanyFinances(models.Model):
    profit = models.FloatField(blank=True, null=False, default=0)
    revenue = models.FloatField(blank=True, null=False, default=0)
    expenses = models.FloatField(blank=True, null=False, default=0)
