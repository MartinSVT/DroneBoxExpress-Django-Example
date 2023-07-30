from django import forms
from DroneBoxExpressApp.Operational.models import AirportModel, DroneModel, RoutesModel, FlightModel


class AirportCreateForm(forms.ModelForm):
    class Meta:
        model = AirportModel
        fields = ["airport_name", "iata_code", "longitude", "latitude", "operational_cost", "fuel_cost"]


class AirportEditForm(forms.ModelForm):
    class Meta:
        model = AirportModel
        fields = ["airport_name", "iata_code", "operational_cost", "fuel_cost"]


class DroneCreateForm(forms.ModelForm):
    class Meta:
        model = DroneModel
        fields = ["model_name", "mtow", "range", "fuel_burn_rate"]


class DroneEditForm(forms.ModelForm):
    class Meta:
        model = DroneModel
        fields = ["model_name", "range", "fuel_burn_rate"]


class RouteCreateForm(forms.ModelForm):
    class Meta:
        model = RoutesModel
        fields = ["origin_airport", "destination_airport", "route_drone"]


class FlightCompleteForm(forms.ModelForm):
    class Meta:
        model = FlightModel
        fields = ["flight_status"]
