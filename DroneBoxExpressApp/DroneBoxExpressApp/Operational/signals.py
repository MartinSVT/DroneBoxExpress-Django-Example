from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from DroneBoxExpressApp.Commercial.models import OrdersModel
from DroneBoxExpressApp.Operational.models import FlightModel, RoutesModel, AirportModel, DroneModel
from DroneBoxExpressApp.Core.additional_functions import cancelled_mail, completed_mail
from DroneBoxExpressApp.Core.database_generators import flight_generator
from DroneBoxExpressApp.Common.models import CompanyFinances
from DroneBoxExpressApp.UserAccount.models import DroneBoxUser, DroneBoxProfile


@receiver(pre_save, sender=RoutesModel)
def pre_save_routes(sender, instance, **kwargs):
    if instance.pk:
        updated_route = instance
        previous_route = RoutesModel.objects.get(pk=updated_route.pk)
        if updated_route.origin_airport == previous_route.origin_airport and updated_route.destination_airport == previous_route.destination_airport:
            if updated_route.maximum_capacity >= previous_route.maximum_capacity:
                pass
            else:
                flight_generator(previous_route)
                updated_route.current_capacity = 0
        else:
            flight_generator(previous_route)
            updated_route.current_capacity = 0


@receiver(pre_delete, sender=RoutesModel)
def pre_delete_routes(sender, instance, **kwargs):
    orders = OrdersModel.objects.filter(order_route=instance)
    service_airport_1, created_a_1 = AirportModel.objects.get_or_create(
        airport_name="service_airport_1",
        iata_code="XXA",
        longitude=1,
        latitude=1,
        operational_cost=1
    )
    service_airport_2, created_a_2 = AirportModel.objects.get_or_create(
        airport_name="service_airport_2",
        iata_code="XXB",
        longitude=3,
        latitude=3,
        operational_cost=1
    )
    service_drone, created_d = DroneModel.objects.get_or_create(
        model_name="service_drone",
        mtow=8000000,
        range=8000000,
        fuel_burn_rate=8000000
    )
    service_route, created = RoutesModel.objects.get_or_create(
        origin_airport=service_airport_1,
        destination_airport=service_airport_2,
        route_drone=service_drone,
        distance=500,
    )
    for order in orders:
        if order.order_status == "Pending":
            current_email = order.order_profile.user.email
            order.order_status = "Cancelled"
            cancelled_mail(order.order_profile, order, current_email)
            order.order_route = service_route
            order.save()
            order.delete()
        else:
            order.order_route = service_route
            order.save()


@receiver(post_save, sender=FlightModel)
def post_save_flight(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        if instance.flight_status == "Completed":
            flight_cost = instance.flight_distance * instance.flight_drone.fuel_burn_rate * instance.flight_origin_airport.fuel_cost
            orders = OrdersModel.objects.filter(order_flight=instance, order_status="Scheduled")
            if orders.exists():
                current_quarter = CompanyFinances.objects.last()
                if current_quarter is None:
                    current_quarter = CompanyFinances.objects.create()
                flight_revenue = 0
                for order in orders:
                    temp_profile = order.order_profile
                    temp_profile.total_revenue += order.cost
                    temp_profile.save()
                    order.order_status = "Completed"
                    temp_email = order.order_profile.user.email
                    flight_revenue += order.cost
                    completed_mail(temp_profile, order, temp_email)
                    order.save()
                flight_profit = flight_revenue - flight_cost
                current_quarter.profit += flight_profit
                current_quarter.revenue += flight_revenue
                current_quarter.expenses += flight_cost
                current_quarter.save()


@receiver(post_delete, sender=FlightModel)
def post_delete_flight(sender, instance, **kwargs):
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
    service_airport_1, created_a_1 = AirportModel.objects.get_or_create(
        airport_name="service_airport_1",
        iata_code="XXA",
        longitude=1,
        latitude=1,
        operational_cost=1
    )
    service_airport_2, created_a_2 = AirportModel.objects.get_or_create(
        airport_name="service_airport_2",
        iata_code="XXB",
        longitude=3,
        latitude=3,
        operational_cost=1
    )
    service_drone, created_d = DroneModel.objects.get_or_create(
        model_name="service_drone",
        mtow=8000000,
        range=8000000,
        fuel_burn_rate=8000000
    )
    service_flight, created = FlightModel.objects.get_or_create(
        flight_origin_airport=service_airport_1,
        flight_destination_airport=service_airport_2,
        flight_drone=service_drone,
        flight_distance=2,
        flight_capacity=2,
        flight_status="Cancelled",
        drone_operator=service_pilot_profile
    )
    orders_to_be_deleted = OrdersModel.objects.filter(order_flight=instance)
    if orders_to_be_deleted.exists():
        for order in orders_to_be_deleted:
            if order.order_status == "Scheduled" or order.order_status == "Pending":
                t_profile = order.order_profile
                order.order_status = "Cancelled"
                t_email = order.order_profile.user.email
                cancelled_mail(t_profile, order, t_email)
                order.order_flight = service_flight
                order.save()
                order.delete()
            else:
                order.order_flight = service_flight
                order.save()
