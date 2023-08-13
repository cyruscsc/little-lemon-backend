from django.test import TestCase
from restaurant.models import Menu, Booking

class MenuTestCase(TestCase):
  def test_get_item(self):
    item = Menu.objects.create(title='Ice Cream', price=7, inventory=200)
    self.assertEqual(item, 'Ice Cream - $7.00')
