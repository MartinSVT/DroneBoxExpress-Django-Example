import sys
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save, post_delete, pre_save
from DroneBoxExpressApp.Commercial.models import OrdersModel
from DroneBoxExpressApp.Operational.models import FlightModel
from DroneBoxExpressApp.Core.additional_functions import scheduled_mail
from DroneBoxExpressApp.UserAccount.models import DroneBoxProfile, DroneBoxUser


def get_pilot():
    available_pilot = ''
    pilots = DroneBoxProfile.objects.filter(profile_type="Pilot")
    if pilots.exists():
        max_num = sys.maxsize
        for pilot in pilots:
            pilot_flights = FlightModel.objects.filter(drone_operator=pilot)
            if pilot_flights.exists():
                num = pilot_flights.count()
                if num < max_num:
                    available_pilot = pilot
            else:
                available_pilot = pilot
                break
    else:
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
        available_pilot = service_pilot_profile
    return available_pilot


@receiver(post_delete, sender=OrdersModel)
def post_delete_order(sender, instance, **kwargs):
    if instance.order_status == "Pending":
        order_route = instance.order_route
        order_route.current_capacity -= instance.weight
        order_route.save()


@receiver(pre_save, sender=OrdersModel)
def pre_save_order(sender, instance, **kwargs):
    if instance.pk:
        prev_order_instance = OrdersModel.objects.get(pk=instance.pk)
        if prev_order_instance.order_status == "Pending" and instance.order_status == "Pending":
            previous_route = prev_order_instance.order_route
            new_route = instance.order_route

            if previous_route == new_route:
                previous_route.current_capacity -= prev_order_instance.weight
                previous_route.current_capacity += instance.weight
                if previous_route.current_capacity + 50 >= previous_route.maximum_capacity:
                    new_flight = FlightModel()
                    new_flight.flight_origin_airport = previous_route.origin_airport
                    new_flight.flight_destination_airport = previous_route.destination_airport
                    new_flight.flight_drone = previous_route.route_drone
                    new_flight.flight_distance = previous_route.distance
                    new_flight.flight_capacity = previous_route.current_capacity
                    new_flight.flight_status = "Scheduled"
                    new_flight.drone_operator = get_pilot()
                    new_flight.save()
                    previous_route.current_capacity = 0.0
                    previous_route.save()
                    orders = OrdersModel.objects.filter(order_route=previous_route)
                    for order in orders:
                        if order.order_status == "Pending":
                            if order != prev_order_instance:
                                order.order_status = "Scheduled"
                                order.order_flight = new_flight
                                order.save()
                                current_email = order.order_profile.user.email
                                scheduled_mail(order.order_profile, order, current_email)
                    instance.order_status = "Scheduled"
                    instance.order_flight = new_flight
                    instance.save()
                    instance_email = instance.order_profile.user.email
                    scheduled_mail(instance.order_profile, instance, instance_email)
                else:
                    previous_route.save()
            else:
                previous_route.current_capacity -= prev_order_instance.weight
                previous_route.save()
                new_route.current_capacity += instance.weight
                if new_route.current_capacity + 50 >= new_route.maximum_capacity:
                    new_flight = FlightModel()
                    new_flight.flight_origin_airport = new_route.origin_airport
                    new_flight.flight_destination_airport = new_route.destination_airport
                    new_flight.flight_drone = new_route.route_drone
                    new_flight.flight_distance = new_route.distance
                    new_flight.flight_capacity = new_route.current_capacity
                    new_flight.drone_operator = get_pilot()
                    new_flight.flight_status = "Scheduled"
                    new_flight.save()
                    new_route.current_capacity = 0.0
                    new_route.save()
                    orders = OrdersModel.objects.filter(order_route=new_route)
                    for order in orders:
                        if order.order_status == "Pending":
                            if order != prev_order_instance:
                                order.order_status = "Scheduled"
                                order.order_flight = new_flight
                                order.save()
                                current_email = order.order_profile.user.email
                                scheduled_mail(order.order_profile, order, current_email)
                    instance.order_status = "Scheduled"
                    instance.order_flight = new_flight
                    instance.save()
                    instance_email = instance.order_profile.user.email
                    scheduled_mail(instance.order_profile, instance, instance_email)
                else:
                    new_route.save()


@receiver(post_save, sender=OrdersModel)
def post_save_order(sender, instance, created, **kwargs):
    if created and instance.order_status == "Pending":
        t_route = instance.order_route
        t_route.current_capacity += instance.weight
        if t_route.current_capacity + 50 >= t_route.maximum_capacity:
            new_flight = FlightModel()
            new_flight.flight_origin_airport = t_route.origin_airport
            new_flight.flight_destination_airport = t_route.destination_airport
            new_flight.flight_drone = t_route.route_drone
            new_flight.flight_distance = t_route.distance
            new_flight.flight_capacity = t_route.current_capacity
            new_flight.drone_operator = get_pilot()
            new_flight.flight_status = "Scheduled"
            new_flight.save()
            t_route.current_capacity = 0.0
            t_route.save()
            orders = OrdersModel.objects.filter(order_route=t_route)
            for order in orders:
                if order.order_status == "Pending":
                    if order != instance:
                        order.order_status = "Scheduled"
                        order.order_flight = new_flight
                        order.save()
                        current_email = order.order_profile.user.email
                        scheduled_mail(order.order_profile, order, current_email)
            instance.order_status = "Scheduled"
            instance.order_flight = new_flight
            instance.save()
            instance_email = instance.order_profile.user.email
            scheduled_mail(instance.order_profile, instance, instance_email)
        else:
            t_route.save()

# Optimize the Signals to and cleanup the code
# Add check for weight to avoid unnecessary operations if no changes are made
# Try taking the route from DB not directly from the instance in Post_save
