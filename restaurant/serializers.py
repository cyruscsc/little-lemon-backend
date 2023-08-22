from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Menu, Booking

class UserSerializer(ModelSerializer):
  class Meta():
    model = User
    fields = ['id', 'username', 'email', 'password']

class MenuSerializer(ModelSerializer):
  class Meta():
    model = Menu
    fields = '__all__'

class BookingSerializer(ModelSerializer):
  class Meta():
    model = Booking
    fields = '__all__'
