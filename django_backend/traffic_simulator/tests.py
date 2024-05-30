# file: traffic_simulator/tests.py
from django.test import TestCase
from .models import TrafficData

class TrafficDataTestCase(TestCase):
  def test_traffic_data_creation(self):
    data = TrafficData.objects.create(source_ip="192.168.1.1", destination_ip="192.168.1.2", bytes_transferred=1234)
    self.assertEqual(data.source_ip, "192.168.1.1")
