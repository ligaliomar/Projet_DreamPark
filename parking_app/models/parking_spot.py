from django.db import models

class ParkingSpot(models.Model):
    """
    Représente une place de parking.
    """
    identifier = models.CharField(max_length=10, unique=True)
    level = models.IntegerField()
    max_length = models.FloatField()
    max_height = models.FloatField()
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.identifier} (Niveau {self.level})"