from django.db import models

class TrafficData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    source_ip = models.CharField(max_length=15)
    destination_ip = models.CharField(max_length=15)
    bytes_transferred = models.BigIntegerField()

    def __str__(self):
        return f"{self.source_ip} to {self.destination_ip} - {self.bytes_transferred} bytes"

