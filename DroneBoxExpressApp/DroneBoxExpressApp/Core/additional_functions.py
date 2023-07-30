from math import radians, cos, sin, asin, sqrt
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from DroneBoxExpressApp import settings


# To be linked with a price API to have always current price
fuel_cost = 2.15


def distance_calculator(lat1, lon1, lat2, lon2):
    earth_radius = 6371

    rad_lat1 = radians(lat1)
    rad_lat2 = radians(lat2)
    rad_lon1 = radians(lon1)
    rad_lon2 = radians(lon2)

    dist_lon = rad_lon2 - rad_lon1
    dist_lat = rad_lat2 - rad_lat1
    a = sin(dist_lat / 2)**2 + cos(rad_lat1) * cos(rad_lat2) * sin(dist_lon / 2)**2
    c = 2 * asin(sqrt(a))
    result = round((c * earth_radius), 1)

    return result


def scheduled_mail(profile, order, email):
    subject = 'Order Status Changed'
    html_message = render_to_string('email_pending.html', {'profile': profile, "order": order})
    plain_message = strip_tags(html_message)
    to = email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to],
        html_message=html_message
    )


def cancelled_mail(profile, order, email):
    subject = 'Order has been Cancelled'
    html_message = render_to_string('email_cancelled.html', {'profile': profile, "order": order})
    plain_message = strip_tags(html_message)
    to = email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to],
        html_message=html_message
    )


def completed_mail(profile, order, email):
    subject = 'Order has been Completed'
    html_message = render_to_string('email_completed.html', {'profile': profile, "order": order})
    plain_message = strip_tags(html_message)
    to = email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to],
        html_message=html_message
    )
