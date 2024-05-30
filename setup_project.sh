#!/bin/bash

# Create the Django backend directory and subdirectories
mkdir -p django_backend/traffic_simulator
cd django_backend

# Create Django project and application
django-admin startproject traffic_analytics .
cd traffic_analytics
django-admin startapp traffic_simulator ../traffic_simulator

# Navigate back to the root django_backend directory
cd ..

# Create initial files
echo "from django.db import models

class TrafficData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    source_ip = models.CharField(max_length=15)
    destination_ip = models.CharField(max_length=15)
    bytes_transferred = models.BigIntegerField()

    def __str__(self):
        return f\"{self.source_ip} to {self.destination_ip} - {self.bytes_transferred} bytes\"
" > traffic_simulator/models.py

echo "from rest_framework import serializers
from .models import TrafficData

class TrafficDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficData
        fields = '__all__'
" > traffic_simulator/serializers.py

echo "from django.contrib import admin
from .models import TrafficData

admin.site.register(TrafficData)
" > traffic_simulator/admin.py

echo "from rest_framework import viewsets
from .models import TrafficData
from .serializers import TrafficDataSerializer

class TrafficDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrafficData.objects.all()
    serializer_class = TrafficDataSerializer
" > traffic_simulator/views.py

echo "Django
djangorestframework
clickhouse-connect
" > requirements.txt

# Create the React frontend directory
mkdir -p ../../traffic-analytics-frontend
cd ../../traffic-analytics-frontend

# Create React app
npx create-react-app . --template typescript

# Create components and stores directories
mkdir -p src/components src/stores

# Create the Docker and CI/CD configuration files
cd ..
echo "FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

CMD [\"python\", \"manage.py\", \"runserver\", \"0.0.0.0:8000\"]
" > Dockerfile

echo "version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - \"8000:8000\"
    depends_on:
      - db
  db:
    image: yandex/clickhouse-server
    ports:
      - \"8123:8123\"
      - \"9000:9000\"
" > docker-compose.yml

echo "stages:
  - test
  - deploy

test_backend:
  stage: test
  image: python:3.9-slim
  script:
    - pip install -r requirements.txt
    - python manage.py test

deploy_to_production:
  stage: deploy
  image: docker:19.03.12
  services:
    - docker:19.03.12-dind
  script:
    - docker login -u \"\$CI_REGISTRY_USER\" -p \"\$CI_REGISTRY_PASSWORD\" \$CI_REGISTRY
    - docker build -t my-django-app .
    - docker push my-django-app
" > .gitlab-ci.yml

echo "Project setup complete."

