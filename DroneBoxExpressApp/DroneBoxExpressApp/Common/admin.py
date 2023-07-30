from django.contrib import admin
from DroneBoxExpressApp.Common.models import NewsModel


class NewsModelAdmin(admin.ModelAdmin):
    list_display = ["article_title", "article_content", "article_author", "article_author_key"]


admin.site.register(NewsModel, NewsModelAdmin)
