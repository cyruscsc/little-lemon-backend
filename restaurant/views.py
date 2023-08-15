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
class MenuView(generics.ListCreateAPIView):
  queryset = Menu.objects.all()
  serializer_class = MenuSerializer
  search_fields = ['title','category__title']
  ordering_fields = ['price']

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

  def get_queryset(self):
    if self.request.user.groups.filter(name='Manager').exists():
      queryset = Booking.objects.all()
    else:
      queryset = Booking.objects.filter(user=self.request.user)
    return queryset

  def post(self, request, *args, **kwargs):
    try:
      Booking.objects.create(
        user=request.user,
        num_guests=request.data['num_guests'],
        date=request.data['date'],
        time=request.data['time']
        )
    except:
      return JsonResponse(status=400, data={'message': 'Booking failed'})
    return JsonResponse(status=201, data={'message': 'Booking successful'})

class SingleBookingView(generics.RetrieveDestroyAPIView):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer
  permission_class = [IsAuthenticated]

  def get_queryset(self):
    if self.request.user.groups.filter(name='Manager').exists():
      queryset = Booking.objects.all()
    else:
      queryset = Booking.objects.filter(user=self.request.user)
    return queryset
