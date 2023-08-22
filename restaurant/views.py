from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Menu, Booking
from .serializers import UserSerializer, MenuSerializer, BookingSerializer
from .permissions import IsManager

# Create your views here.
def csrfView(request):
  token = get_token(request)
  return JsonResponse(status=200, data={'csrf_token': token})

class CheckUsernameView(APIView):
  def post(self, request, *args, **kwargs):
    username = request.data['username']
    if User.objects.filter(username=username).exists():
      return JsonResponse(data={'available': False, 'message': 'Username already in use'})
    else:
      return JsonResponse(data={'available': True, 'message': ''})

class CheckEmailView(APIView):
  def post(self, request, *args, **kwargs):
    email = request.data['email']
    if User.objects.filter(email=email).exists():
      return JsonResponse(data={'available': False, 'message': 'Email already in use'})
    else:
      return JsonResponse(data={'available': True, 'message': ''})

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
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return JsonResponse(status=200, data={'message': 'Logged in successfully'})
    else:
      return JsonResponse(status=400, data={'message': 'Invalid username or password'})

def logoutView(request):
  if request.user.is_authenticated:
    logout(request)
    return JsonResponse(status=200, data={'message': 'Logged out successfully'})
  else:
    return JsonResponse(status=400, data={'message': "It's hard to log out before log in"})

class SessionView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kwargs):
    return JsonResponse(status=200, data={'session_exists': True})

class UserView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kwargs):
    return JsonResponse(status=200, data={
      'username': request.user.username,
      'email': request.user.email
    })

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
