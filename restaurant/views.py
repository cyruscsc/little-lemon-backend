from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from datetime import datetime
from .models import Menu, Booking
from .serializers import UserSerializer, MenuSerializer, BookingSerializer
from .permissions import IsManager
from .jwtauth import JwtToken, ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY
import jwt, datetime

jwt_secret = 'This is not a secret'

# Create your views here.
class RegisterView(APIView):
  def post(self, request, *args, **kwargs):
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']

    # Create user
    user_data = {
      'username': username,
      'email': email,
      'password': make_password(password)
    }
    serializer = UserSerializer(data=user_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    user = authenticate(username=username, password=password)
    jwt_token = JwtToken(request)
    jwt_token.issue(user.id, user.username, user.email, user.is_staff)

    response = Response()
    response.set_cookie(key=ACCESS_TOKEN_COOKIE_KEY, value=jwt_token.access_token, httponly=True)
    response.set_cookie(key=REFRESH_TOKEN_COOKIE_KEY, value=jwt_token.refresh_token, httponly=True)
    response.data = {
      'message': f'User created, logged in as {username} successfully',
    }
    return response

class LoginView(APIView):
  def post(self, request, *args, **kwargs):
    username = request.data['username']
    password = request.data['password']

    try:
      user = authenticate(username=username, password=password)
    except:
      raise AuthenticationFailed('Invalid username or password')
    jwt_token = JwtToken(request)
    jwt_token.issue(user.id, user.username, user.email, user.is_staff)

    response = Response()
    response.set_cookie(key=ACCESS_TOKEN_COOKIE_KEY, value=jwt_token.access_token, httponly=True)
    response.set_cookie(key=REFRESH_TOKEN_COOKIE_KEY, value=jwt_token.refresh_token, httponly=True)
    response.data = {
      'message': f'Logged in as {username} successfully',
    }
    return response

class LogoutView(APIView):
  def post(self, request, *args, **kwargs):
    response = Response()
    response.delete_cookie(ACCESS_TOKEN_COOKIE_KEY)
    response.delete_cookie(REFRESH_TOKEN_COOKIE_KEY)
    response.data = {
      'message': 'Logged out successfully',
    }
    return response

class UserView(APIView):
  def get(self, request, *args, **kwargs):
    jwt_token = JwtToken(request)
    if jwt_token.is_valid():
      user_id, username, email, is_staff = jwt_token.get_user()
    else:
      raise AuthenticationFailed('Unauthenticated user')

    response = Response()
    response.data = {
      'user_id': user_id,
      'username': username,
      'email': email,
      'is_staff': is_staff,
    }
    response.set_cookie(key=ACCESS_TOKEN_COOKIE_KEY, value=jwt_token.access_token, httponly=True)
    response.set_cookie(key=REFRESH_TOKEN_COOKIE_KEY, value=jwt_token.refresh_token, httponly=True)
    return response

class MenuView(generics.ListAPIView):
  queryset = Menu.objects.all()
  serializer_class = MenuSerializer
  search_fields = ['title','category__title']
  ordering_fields = ['price']

class MenuItemView(generics.RetrieveAPIView):
  queryset = Menu.objects.all()
  serializer_class = MenuSerializer

class BookingsView(generics.ListCreateAPIView):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer

  def get_queryset(self):
    jwt_token = JwtToken(self.request)
    if jwt_token.is_valid():
      user_id, username, email, is_staff = jwt_token.get_user()
    else:
      raise AuthenticationFailed('Unauthenticated user')

    if is_staff:
      queryset = Booking.objects.all()
    else:
      queryset = Booking.objects.filter(user_id=user_id)
    return queryset

  def post(self, request, *args, **kwargs):
    jwt_token = JwtToken(request)
    if jwt_token.is_valid():
      user_id, username, email, is_staff = jwt_token.get_user()
    else:
      raise AuthenticationFailed('Unauthenticated user')

    try:
      Booking.objects.create(
        user_id=user_id,
        email=request.data['email'],
        num_guests=request.data['num_guests'],
        date=request.data['date'],
        time=request.data['time']
        )
    except:
      response = Response(status=status.HTTP_400_BAD_REQUEST)
      response.data = {
        'message': 'Booking failed',
      }
      return response
    response = Response(status=status.HTTP_201_CREATED)
    response.data = {
      'message': 'Booking successful',
    }
    return response

class SingleBookingView(generics.RetrieveDestroyAPIView):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer

  def get_queryset(self):
    jwt_token = JwtToken(self.request)
    if jwt_token.is_valid():
      user_id, username, email, is_staff = jwt_token.get_user()
    else:
      raise AuthenticationFailed('Unauthenticated user')

    if is_staff:
      queryset = Booking.objects.all()
    else:
      queryset = Booking.objects.filter(user_id=user_id)
    return queryset
