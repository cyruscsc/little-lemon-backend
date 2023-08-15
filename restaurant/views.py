from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer
from .permissions import IsManager

# Create your views here.
class IndexView(TemplateView):
  template_name = 'index.html'

class MenuView(generics.ListCreateAPIView):
  queryset = Menu.objects.all()
  serializer_class = MenuSerializer

  def get_permissions(self):
    if self.request.method != 'GET':
      permission_classes = [IsManager]
      return [permission() for permission in permission_classes]
    else:
      return []

class MenuItemView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Menu.objects.all()
  serializer_class = MenuSerializer

  def get_permissions(self):
    if self.request.method != 'GET':
      permission_classes = [IsManager]
      return [permission() for permission in permission_classes]
    else:
      return []

class BookingsView(generics.ListCreateAPIView):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kwargs):
    user = request.user
    num_guests = request.data['num_guests']
    date = request.data['date']
    time = request.data['time']
    try:
      date_split = [int(string) for string in date.split('-')]
      time_split = [int(string) for string in time.split(':')]
      date_time = datetime(date_split[0], date_split[1], date_split[2], time_split[0], time_split[1])
      Booking.objects.create(user=user, num_guests=num_guests, booking_date=date_time)
    except:
      return JsonResponse(status=400, data={'message': 'Booking failed'})
    return JsonResponse(status=201, data={'message': 'Booking successful'})

class SingleBookingView(generics.RetrieveDestroyAPIView):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer
  permission_class = [IsAuthenticated]
