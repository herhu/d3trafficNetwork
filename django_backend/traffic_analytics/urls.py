# file: traffic_analytics/urls.py (main project)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('traffic_simulator.urls')),
]