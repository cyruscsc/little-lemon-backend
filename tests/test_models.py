from django.test import TestCase
from restaurant.models import Menu, Booking
from datetime import datetime

class MenuModelTestCase(TestCase):
  def setUp(self):
    Menu.objects.create(title='Greek Salad', price=12, inventory=100)
    Menu.objects.create(title='Bruschetta', price=11.5, inventory=80)
    Menu.objects.create(title='Lemon Dessert', price=9.5, inventory=160)

  def test_get_menu_item(self):
    menu_item = Menu.objects.get(pk=2)
    clean_menu_item = str(menu_item)
    self.assertEqual(clean_menu_item, 'Bruschetta - $11.50')

  def test_get_menu_items(self):
    menu_items = Menu.objects.all()
    clean_menu_items = [str(item) for item in menu_items]
    self.assertEqual(clean_menu_items, [
      'Greek Salad - $12.00',
      'Bruschetta - $11.50',
      'Lemon Dessert - $9.50',
      ])

class BookingModelTestCase(TestCase):
  def setUp(self):
    dt1 = datetime(2023, 8, 25, 19, 0, 0, 0)
    dt2 = datetime(2023, 8, 26, 12, 30, 0, 0)
    dt3 = datetime(2023, 8, 30, 18, 0, 0, 0)
    Booking.objects.create(name='Adrian', no_of_guests=6, booking_date=dt1)
    Booking.objects.create(name='Mario', no_of_guests=4, booking_date=dt2)
    Booking.objects.create(name='Karen', no_of_guests=2, booking_date=dt3)

  def test_get_reservation(self):
    reservation = Booking.objects.get(pk=1)
    clean_reservation = str(reservation)
    self.assertEqual(clean_reservation, 'Adrian - 6 guests')

  def test_get_reservations(self):
    reservations = Booking.objects.all()
    clean_reservations = [str(reservation) for reservation in reservations]
    self.assertEqual(clean_reservations, [
      'Adrian - 6 guests',
      'Mario - 4 guests',
      'Karen - 2 guests',
    ])
