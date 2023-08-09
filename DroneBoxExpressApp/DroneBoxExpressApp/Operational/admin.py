from django.contrib import admin
from DroneBoxExpressApp.Operational.models import AirportModel, DroneModel, RoutesModel, FlightModel


# Add further functionality to the admin site to remove editing and deleting already scheduled flights
class AirportAdmin(admin.ModelAdmin):
    list_display = ["airport_name", 'iata_code', "operational_cost", "fuel_cost", "longitude", "latitude"]
    list_filter = ["operational_cost", "fuel_cost"]
    list_display_links = ["airport_name", "iata_code"]
    search_fields = ["airport_name", "iata_code"]
    ordering = ["iata_code"]
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ["longitude", "latitude", "iata_code"]
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False


class DroneAdmin(admin.ModelAdmin):
    list_display = ["model_name", "mtow", "range", "fuel_burn_rate"]
    list_filter = ["model_name"]
    list_display_links = ["model_name"]
    search_fields = ["model_name", "mtow"]
    ordering = ["mtow"]
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ["mtow", "range"]
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False


class FlightAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "drone_operator",
        "flight_origin_airport",
        "flight_destination_airport",
        "flight_drone",
        "flight_status",
        "flight_distance",
        "flight_capacity"
    ]
    list_filter = ("flight_origin_airport", "flight_destination_airport", "flight_drone", "drone_operator")
    search_fields = ("flight_origin_airport", "flight_destination_airport", "flight_drone", "drone_operator")
    list_display_links = ("pk", "flight_origin_airport", "flight_destination_airport", "drone_operator")
    ordering = ["pk", "flight_status"]
    readonly_fields = [
        "pk",
        "flight_origin_airport",
        "flight_destination_airport",
        "flight_distance",
        "flight_capacity",
    ]

    def has_add_permission(self, request):
        return False

    @staticmethod
    def drone_operator(obj):
        return obj.get_custom_name

    def get_form(self, request, obj=None, **kwargs):
        labels = {
            "pk": "Flight Number: "
        }
        kwargs.update({"labels": labels})
        return super(FlightAdmin, self).get_form(request, obj=obj, **kwargs)


class RouteAdmin(admin.ModelAdmin):
    list_display = ['origin_airport', "destination_airport", "route_drone", "current_capacity", "maximum_capacity", "distance"]
    list_filter = ["origin_airport", "destination_airport", "route_drone"]
    list_display_links = ["origin_airport", "destination_airport"]
    ordering = ["current_capacity"]
    search_fields = ["origin_airport", "destination_airport", "route_drone"]


admin.site.register(AirportModel, AirportAdmin)
admin.site.register(DroneModel, DroneAdmin)
admin.site.register(FlightModel, FlightAdmin)
admin.site.register(RoutesModel, RouteAdmin)
