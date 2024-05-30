# file: traffic_simulator/urls.py
from django.urls import path
from traffic_simulator.views import TrafficDataView

urlpatterns = [
    path('api/traffic/', TrafficDataView.as_view(), name='traffic-data'),
]
