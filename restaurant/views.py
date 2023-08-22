from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from datetime import datetime
from .models import Menu, Booking
from .serializers import UserSerializer, MenuSerializer, BookingSerializer
from .permissions import IsManager
import jwt, datetime

jwt_secret = 'This is not a secret'

# Create your views here.
class RegisterView(APIView):
  def post(self, request, *args, **kwargs):
    user_data = {
      'username': request.data['username'],
      'email': request.data['email'],
      'password': make_password(request.data['password'])
    }
    serializer = UserSerializer(data=user_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return JsonResponse(status=200, data={'message': f'User {serializer.validated_data["username"]} created successfully'})

class LoginView(APIView):
  def post(self, request, *args, **kwargs):
    username = request.data['username']
    password = request.data['password']
    try:
      user = authenticate(username=username, password=password)
    except:
      raise AuthenticationFailed('Incorrect username or password')
    access_payload = {
      'user_id': user.id,
      'username': user.username,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
      'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_payload, jwt_secret, algorithm='HS256')
    response = Response()
    response.set_cookie(key='jwtaccess', value=access_token, httponly=True)
    response.data = {
      'jwtaccess': access_token
    }
    return response

class LogoutView(APIView):
  def post(self, request, *args, **kwargs):
    response = Response()
    response.delete_cookie('jwtaccess')
    response.data ={
      'message': 'Logged out successfully'
    }
    return response

class UserView(APIView):
  def get(self, request, *args, **kwargs):
    access_token = request.COOKIES.get('jwtaccess')
    try:
      access_payload = jwt.decode(access_token, jwt_secret, algorithms=['HS256'])
    except:
      raise AuthenticationFailed('Unauthenticated user')
    user = User.objects.filter(id=access_payload['user_id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)

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
