from django.db import models

class ParkingSpot(models.Model):
    """
    Classe qui represente une place de parking
    Chaque place a un identifiant unique comme demande dans le sujet
    """
    # Identifiant unique de la place (ex: A12, B05...)
    numero_place = models.CharField(max_length=10, unique=True)
    # Niveau de la place dans le parking
    niveau = models.IntegerField()
    # Dimensions maximales acceptees
    longueur_max = models.FloatField()
    hauteur_max = models.FloatField()
    # Si la place est occupee ou pas
    est_occupee = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero_place} (Niveau {self.niveau})"