from enum import Enum
from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from DroneBoxExpressApp.Core.additional_functions import distance_calculator, fuel_cost
from DroneBoxExpressApp.Core.mixins import EnumMixin
from DroneBoxExpressApp.UserAccount.models import DroneBoxProfile


class FlightStatus(EnumMixin, Enum):
    Scheduled = "Scheduled"
    Completed = "Completed"
    Cancelled = "Cancelled"


class DroneModel(models.Model):
    model_name = models.CharField(blank=False, null=False, max_length=30)
    mtow = models.PositiveIntegerField(blank=False, null=False, validators=[MaxValueValidator(9000000)])
    range = models.PositiveIntegerField(blank=False, null=False, validators=[MaxValueValidator(9000000)])
    fuel_burn_rate = models.FloatField(blank=False, null=False, validators=[
        MinValueValidator(0.0),
        MaxValueValidator(9000000)
    ])

    def __str__(self):
        return self.model_name


class AirportModel(models.Model):
    airport_name = models.CharField(blank=False, null=False, max_length=50)
    iata_code = models.CharField(
        blank=False,
        null=False,
        max_length=3,
        validators=[MinLengthValidator(3)]
    )
    longitude = models.FloatField(blank=False, null=False)
    latitude = models.FloatField(blank=False, null=False)
    operational_cost = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])
    fuel_cost = models.FloatField(blank=True, null=False, default=fuel_cost, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f'({self.iata_code}) {self.airport_name}'


class RoutesModel(models.Model):
    origin_airport = models.ForeignKey(
        to=AirportModel,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        related_name='Route_Origin_Airport'
    )
    destination_airport = models.ForeignKey(
        to=AirportModel,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        related_name='Route_Destination_Airport'
    )
    route_drone = models.ForeignKey(
        to=DroneModel,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False
    )
    maximum_capacity = models.FloatField(
        validators=[MinValueValidator(0.0)],
        editable=False,
        blank=False,
        null=False
    )
    current_capacity = models.FloatField(
        blank=True,
        null=False,
        default=0.0,
        validators=[MinValueValidator(0.0)]
    )
    distance = models.FloatField(editable=False, blank=False, null=False, validators=[MinValueValidator(0.0)])

    def clean(self):
        distance = distance_calculator(
            self.origin_airport.latitude,
            self.origin_airport.longitude,
            self.destination_airport.latitude,
            self.destination_airport.longitude
        )
        if distance < 1:
            raise ValidationError("Origin Airport is the same as Destination Airport")
        else:
            self.distance = distance

    def save(self, *args, **kwargs):
        self.maximum_capacity = self.route_drone.mtow
        super(RoutesModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.origin_airport} to {self.destination_airport}"


class FlightModel(models.Model):
    flight_origin_airport = models.ForeignKey(
        to=AirportModel,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        related_name='Flight_Origin_Airport'
    )
    flight_destination_airport = models.ForeignKey(
        to=AirportModel,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        related_name='Flight_Destination_Airport'
    )
    flight_drone = models.ForeignKey(
        to=DroneModel,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False
    )
    flight_distance = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])
    flight_capacity = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])
    flight_status = models.CharField(
        choices=FlightStatus.list_choices(),
        max_length=FlightStatus.max_len(),
        default="Scheduled",
        null=False,
        blank=False,
    )
    drone_operator = models.ForeignKey(
        to=DroneBoxProfile,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False
    )

    def __str__(self):
        return f"{self.flight_origin_airport} to {self.flight_destination_airport}"
