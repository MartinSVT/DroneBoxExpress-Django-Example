import sys
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


def flight_generator(temp_route):
    orders = OrdersModel.objects.filter(order_route=temp_route, order_status="Pending")
    if orders.exists():
        temp_flight = FlightModel()
        temp_flight.flight_origin_airport = temp_route.origin_airport
        temp_flight.flight_destination_airport = temp_route.destination_airport
        temp_flight.flight_drone = temp_route.route_drone
        temp_flight.flight_distance = temp_route.distance
        temp_flight.flight_capacity = temp_route.current_capacity
        temp_flight.drone_operator = get_pilot()
        temp_flight.flight_status = "Scheduled"
        temp_flight.save()
        for order in orders:
            order.order_status = "Scheduled"
            order.order_flight = temp_flight
            order.save()
            current_email = order.order_profile.user.email
            scheduled_mail(order.order_profile, order, current_email)
        return temp_flight
