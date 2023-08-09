from django.contrib import admin
from DroneBoxExpressApp.Commercial.models import OrdersModel, PricesModel, DiscountsModel
from DroneBoxExpressApp.Commercial.forms import PricesAddForm, DiscountAddForm


class OrdersAdmin(admin.ModelAdmin):
    list_display = ["order_profile", "order_route", "order_status", "cost", "order_flight", "order_type", "weight"]
    exclude = ["order_status", "order_flight"]
    readonly_fields = ["order_profile", "order_route", "order_status", "cost", "order_flight", "order_type", "weight"]
    list_filter = ["order_profile", "order_status", "order_flight", "order_route"]
    list_display_links = ["order_profile", "order_route", "order_status", "order_flight"]
    search_fields = ["order_profile", "order_route", "order_status", "cost", "order_flight", "order_type", "weight"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PricesAdmin(admin.ModelAdmin):
    list_display = ["target_order_type", "min_weight", "max_weight", "price_per_kg"]
    form = PricesAddForm
    ordering = ["target_order_type"]
    list_filter = ["target_order_type"]
    list_display_links = ["target_order_type", "min_weight", "max_weight", "price_per_kg"]
    search_fields = ["target_order_type", "min_weight", "max_weight", "price_per_kg"]


class DiscountsAdmin(admin.ModelAdmin):
    list_display = ["discount_profile_type", "min_profile_revenue", "max_profile_revenue", "discount_rate"]
    form = DiscountAddForm
    ordering = ["discount_profile_type"]
    list_filter = ["discount_profile_type"]
    list_display_links = ["discount_profile_type", "min_profile_revenue", "max_profile_revenue", "discount_rate"]
    search_fields = ["discount_profile_type", "min_profile_revenue", "max_profile_revenue", "discount_rate"]


admin.site.register(OrdersModel, OrdersAdmin)
admin.site.register(PricesModel, PricesAdmin)
admin.site.register(DiscountsModel, DiscountsAdmin)
