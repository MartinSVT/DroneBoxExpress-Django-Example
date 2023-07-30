from django.urls import path
from DroneBoxExpressApp.Operational import views

urlpatterns = [
    path('', views.OperationalView.as_view(), name='Operations-Page'),
    path('airports/add/', views.CreateAirportView.as_view(), name='Create-Airport-Page'),
    path('airports/edit/<int:pk>/', views.EditAirportView.as_view(), name='Edit-Airport-Page'),
    path('drones/add/', views.CreateDroneView.as_view(), name='Create-Drone-Page'),
    path('drones/edit/<int:pk>/', views.EditDroneView.as_view(), name='Edit-Drone-Page'),
    path('routes/add/', views.CreateRouteView.as_view(), name='Create-Route-Page'),
    path('routes/edit/<int:pk>', views.EditRouteView.as_view(), name='Edit-Route-Page'),
    path('routes/delete/<int:pk>', views.DeleteRouteView.as_view(), name='Delete-Route-Page'),
    path('routes/rest/<int:pk>/', views.DetailsRouteRESTView.as_view(), name='Details-Route-REST'),
    path('flights/edit/<int:pk>', views.EditFlightsView.as_view(), name='Edit-Flight-Page'),
    path('flights/delete/<int:pk>', views.DeleteFlightsView.as_view(), name='Delete-Flight-Page'),
]
