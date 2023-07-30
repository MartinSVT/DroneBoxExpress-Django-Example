from django.urls import path
from DroneBoxExpressApp.UserAccount import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='Register'),
    path('login/', views.UserLoginView.as_view(), name='Login'),
    path('logout/', views.UserLogoutView.as_view(), name='Logout'),
    path('profile/<int:pk>/', views.ProfileDetailsView.as_view(), name='Profile-Details'),
    path('profile/edit/<int:pk>/', views.ProfileEdithView.as_view(), name='Profile-Edit'),
    path('profile/delete/<int:pk>/', views.ProfileDeleteView.as_view(), name='Profile-Delete'),
]
