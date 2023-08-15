from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
  path('', views.IndexView.as_view()),
  path('api/menu', views.MenuView.as_view()),
  path('api/menu/<int:pk>', views.MenuItemView.as_view()),
  path('api/bookings', views.BookingsView.as_view()),
  path('api-token-auth', obtain_auth_token),
]
