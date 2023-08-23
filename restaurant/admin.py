from django.contrib import admin
from .models import Category, Menu, Booking

# Register your models here.
admin.site.register([Category, Menu, Booking])
