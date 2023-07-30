from django.urls import path
from DroneBoxExpressApp.Commercial import views

urlpatterns = [
    path('', views.OrdersView.as_view(), name='Orders-Page'),
    path('add/', views.CreateOrderView.as_view(), name='Create-Order-Page'),
    path('details/<int:pk>/', views.DetailsOrderView.as_view(), name='Details-Order-Page'),
    path('delete/<int:pk>/', views.DeleteOrderView.as_view(), name='Delete-Order-Page'),
    path('update/<int:pk>/', views.UpdateOrderView.as_view(), name='Update-Order-Page'),
    path('prices/', views.PricesListCreateView.as_view(), name='Prices-Page'),
    path('prices/<int:pk>/', views.PricesUpdateDeleteView.as_view(), name='Prices-Delete-Update-Page'),
    path('discounts/', views.DiscountsListCreateView.as_view(), name='Discount-Page'),
    path('discounts/<int:pk>/', views.DiscountsUpdateDeleteView.as_view(), name='Discount-Delete-Update-Page'),
]
