from django.db import models
from .parking_spot import ParkingSpot

class Vehicle(models.Model):
    """
    Représente un véhicule entrant dans le parking.
    """
    plate_number = models.CharField(max_length=20)
    length = models.FloatField()
    height = models.FloatField()
    entry_time = models.DateTimeField(auto_now_add=True)

    assigned_spot = models.OneToOneField(
        ParkingSpot,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.plate_number