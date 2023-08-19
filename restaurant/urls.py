from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
  path('csrf', views.csrfView),
  path('register', views.RegisterView.as_view()),
  path('login', views.loginView),
  path('logout', views.logoutView),
  path('session', views.SessionView.as_view()),
  path('user', views.UserView.as_view()),
  path('menu', views.MenuView.as_view()),
  path('menu/<int:pk>', views.MenuItemView.as_view()),
  path('bookings', views.BookingsView.as_view()),
  path('bookings/<int:pk>', views.SingleBookingView.as_view()),
]
