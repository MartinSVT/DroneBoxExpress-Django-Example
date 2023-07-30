from enum import Enum
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from DroneBoxExpressApp.Core.mixins import EnumMixin
from DroneBoxExpressApp.UserAccount.models import ProfileTypes, DroneBoxProfile
from DroneBoxExpressApp.Operational.models import RoutesModel, FlightModel


class OrderType(EnumMixin, Enum):
    Letter = "Letter"
    Parcel = "Parcel"
    Box = "Box"


class OrderStatus(EnumMixin, Enum):
    Pending = "Pending"
    Scheduled = "Scheduled"
    Completed = "Completed"
    Cancelled = "Cancelled"


class OrdersModel(models.Model):
    weight = models.FloatField(
        blank=False,
        null=False,
        validators=(
            MinValueValidator(0.0),
            MaxValueValidator(50.0),
        )
    )
    order_type = models.CharField(
        choices=OrderType.list_choices(),
        max_length=OrderType.max_len(),
        null=False,
        blank=False,
    )
    order_route = models.ForeignKey(
        to=RoutesModel,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
    )
    cost = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])
    order_status = models.CharField(
        choices=OrderStatus.list_choices(),
        max_length=OrderStatus.max_len(),
        default="Pending",
        null=False,
        blank=False,
    )
    order_profile = models.ForeignKey(
        to=DroneBoxProfile,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False
    )
    order_flight = models.ForeignKey(
        to=FlightModel,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )


# ----------- Models used with Django REST API via JS ------------
class PricesModel(models.Model):
    min_weight = models.PositiveIntegerField(blank=False, null=False)
    max_weight = models.PositiveIntegerField(blank=False, null=False)
    price_per_kg = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])
    target_order_type = models.CharField(
        choices=OrderType.list_choices(),
        max_length=OrderType.max_len(),
        null=False,
        blank=False,
    )


class DiscountsModel(models.Model):
    min_profile_revenue = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])
    max_profile_revenue = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])
    discount_rate = models.FloatField(
        blank=False,
        null=False,
        validators=(
            MinValueValidator(0.0),
            MaxValueValidator(1.0),
        ))
    discount_profile_type = models.CharField(
        choices=ProfileTypes.list_choices(),
        max_length=ProfileTypes.max_len(),
        null=False,
        blank=False,
    )
