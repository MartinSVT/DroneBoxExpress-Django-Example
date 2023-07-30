from django.dispatch import Signal, receiver
from django.db.models.signals import post_save, post_delete, pre_delete
from DroneBoxExpressApp.UserAccount.models import DroneBoxProfile, DroneBoxUser
from DroneBoxExpressApp.Commercial.models import OrdersModel
from DroneBoxExpressApp.Operational.models import FlightModel


@receiver(post_save, sender=DroneBoxUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = DroneBoxProfile()
        profile.user = instance
        if instance.is_superuser:
            profile.profile_type = "Admin"
        profile.save()


@receiver(post_save, sender=DroneBoxUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_staff:
        profile = DroneBoxProfile.objects.get(pk=instance.pk)
        profile.profile_type = "Editor"
        profile.save()


@receiver(post_delete, sender=DroneBoxProfile)
def delete_profile(sender, instance, **kwargs):
    # Take the service_user if exist or create it
    service_user, created = DroneBoxUser.objects.get_or_create(
        username="service_user",
        email="serviceUserBG123asdsad123@gmail.com",
    )
    if created:
        service_user.set_password("1a2b3c5d5vBG")
        service_user.save()
    # Take the service_profile
    service_profile = DroneBoxProfile.objects.get(pk=service_user.pk)
    # Take all orders for the deleted profile
    orders = OrdersModel.objects.filter(order_profile_id=instance.pk)
    # Check if each order is Scheduled if so transfer it to the service user else delete it
    if orders.exists():
        for order in orders:
            if order.order_status == "Scheduled":
                order.order_profile = service_profile
                order.save()
            else:
                order.delete()
    # Delete the user associated with the deleted profile
    users = DroneBoxUser.objects.filter(pk=instance.pk)
    if users.exists():
        for user in users:
            user.delete()


@receiver(pre_delete, sender=DroneBoxProfile)
def pre_delete_profile(sender, instance, **kwargs):
    if instance.profile_type == "Pilot":
        service_pilot, created = DroneBoxUser.objects.get_or_create(
            username="service_pilot",
            email="servicePiloBG123asdsad123@gmail.com",
        )
        if created:
            service_pilot.set_password("1a2b3c5d5vBG")
            service_pilot.save()
        service_pilot_profile = DroneBoxProfile.objects.get(pk=service_pilot.pk)
        service_pilot_profile.profile_type = "Pilot"
        service_pilot_profile.save()
        flights = FlightModel.objects.filter(drone_operator=instance)
        if flights.exists():
            for flight in flights:
                flight.drone_operator = service_pilot_profile
                flight.save()
