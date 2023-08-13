from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('api/menu', views.MenuView.as_view(), name='menu'),
  path('api/menu/<int:pk>', views.MenuItemView.as_view(), name='menu-item'),
  path('api/booking', views.BookingView.as_view(), name='booking'),
  path('api-token-auth', obtain_auth_token),
]
