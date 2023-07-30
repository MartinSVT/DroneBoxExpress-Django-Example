from django.contrib import admin
from DroneBoxExpressApp.Commercial.models import OrdersModel, PricesModel, DiscountsModel


class OrdersAdmin(admin.ModelAdmin):
    list_display = ["order_profile", "order_route", "order_status", "cost"]
    exclude = ["order_status"]


class PricesAdmin(admin.ModelAdmin):
    list_display = ["min_weight", "max_weight", "price_per_kg", "target_order_type"]


class DiscountsAdmin(admin.ModelAdmin):
    list_display = ["min_profile_revenue", "max_profile_revenue", "discount_rate", "discount_profile_type"]


admin.site.register(OrdersModel, OrdersAdmin)
admin.site.register(PricesModel, PricesAdmin)
admin.site.register(DiscountsModel, DiscountsAdmin)
