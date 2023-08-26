from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Category, Menu, Booking

class UserSerializer(ModelSerializer):
  class Meta():
    model = User
    fields = ['id', 'username', 'email', 'password']

class CategorySerializer(ModelSerializer):
  class Meta:
    model = Category
    fields = ['title',]

class MenuSerializer(ModelSerializer):
  category = CategorySerializer()

  class Meta():
    model = Menu
    fields = '__all__'

class BookingSerializer(ModelSerializer):
  class Meta():
    model = Booking
    fields = '__all__'
