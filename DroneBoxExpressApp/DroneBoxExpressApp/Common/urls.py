from django.urls import path
from DroneBoxExpressApp.Common import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='Home-Page'),
    path('denied/', views.AccessDeniedView.as_view(), name='Access-Denied-Page'),
    path('contacts/', views.ContactsView.as_view(), name='Contacts-Page'),
    path('aboutus/', views.AboutUsView.as_view(), name='About-Us-Page'),
    path('news/add/', views.NewsCreateView.as_view(), name='News-Create-Page'),
    path('news/edit/<int:pk>/', views.NewsEditView.as_view(), name='News-Edit-Page'),
    path('news/delete/<int:pk>/', views.NewsDeleteView.as_view(), name='News-Delete-Page')
]
