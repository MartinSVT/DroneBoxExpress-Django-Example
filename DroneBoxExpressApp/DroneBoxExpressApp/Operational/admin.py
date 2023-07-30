from django.contrib import admin
from DroneBoxExpressApp.Operational.models import AirportModel, DroneModel, RoutesModel, FlightModel


# Add further functionality to the admin site to remove editing and deleting already scheduled flights
class AirportAdmin(admin.ModelAdmin):
    list_display = ["airport_name", 'iata_code', "operational_cost"]


class DroneAdmin(admin.ModelAdmin):
    list_display = ["model_name", "mtow", "range"]


class FlightAdmin(admin.ModelAdmin):
    list_display = ["pk", "flight_origin_airport", "flight_destination_airport", "flight_drone", "flight_distance"]


class RouteAdmin(admin.ModelAdmin):
    list_display = ['origin_airport', "destination_airport", "route_drone", "maximum_capacity", "current_capacity", "distance"]


admin.site.register(AirportModel, AirportAdmin)
admin.site.register(DroneModel, DroneAdmin)
admin.site.register(FlightModel, FlightAdmin)
admin.site.register(RoutesModel, RouteAdmin)
