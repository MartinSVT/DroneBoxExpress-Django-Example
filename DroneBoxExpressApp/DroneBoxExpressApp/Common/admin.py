from django.contrib import admin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from DroneBoxExpressApp.Common.models import NewsModel, CompanyFinances
from DroneBoxExpressApp.UserAccount.models import DroneBoxProfile


class NewsModelAdmin(admin.ModelAdmin):
    list_display = ["article_title", "article_content", "article_author", "created_date", "updated_date"]
    list_filter = ["article_author"]
    list_display_links = ["article_title", "article_content"]
    search_fields = ["article_title", "article_content"]
    exclude = ["article_author", "article_author_key"]

    def save_model(self, request, obj, form, change):
        try:
            profile = get_object_or_404(DroneBoxProfile, pk=request.user.pk)
        except Http404:
            return redirect("Access-Denied-Page")
        obj.article_author = profile.get_custom_name()
        obj.article_author_key = profile.pk
        super().save_model(request, obj, form, change)


class FinancesAdmin(admin.ModelAdmin):
    list_display = ["revenue", "expenses", "profit"]
    list_display_links = ["revenue", "expenses", "profit"]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(NewsModel, NewsModelAdmin)
admin.site.register(CompanyFinances, FinancesAdmin)