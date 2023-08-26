from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
  slug = models.SlugField()
  title = models.CharField(db_index=True, max_length=255)

  def __str__(self) -> str:
    return self.title

class Menu(models.Model):
  title = models.CharField(db_index=True, max_length=255)
  description = models.TextField(max_length=2000)
  price = models.DecimalField(db_index=True, max_digits=5, decimal_places=2)
  featured = models.BooleanField(db_index=True)
  category = models.ForeignKey(Category, on_delete=models.PROTECT)

  def __str__(self) -> str:
    return self.title

class Booking(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  email = models.EmailField()
  num_guests = models.IntegerField()
  date = models.DateField()
  time = models.TimeField()

  def __str__(self) -> str:
    return f"{self.user} - {self.num_guests} guests"
