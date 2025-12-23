from django.db import models
from .parking_spot import ParkingSpot

class Vehicle(models.Model):
    """
    Classe pour representer une voiture qui entre dans le parking
    J'ai mis tous les attributs demandes dans le sujet
    """
    class SubscriptionType(models.TextChoices):
        NONE = "NONE", "Client occasionnel"
        STANDARD = "STANDARD", "Abonné"
        GUARANTEED = "GUARANTEED", "Pack garanti"
    
    # Immatriculation du vehicule
    plaque_immat = models.CharField(max_length=20)
    # Dimensions de la voiture (en metres)
    longueur = models.FloatField()
    hauteur = models.FloatField()
    # Heure d'entree dans le parking
    heure_entree = models.DateTimeField(auto_now_add=True)
    # Type d'abonnement (par defaut client occasionnel)
    type_abonnement = models.CharField(
        max_length=20,
        choices=SubscriptionType.choices,
        default=SubscriptionType.NONE
    )

    # La place assignee au vehicule (peut etre vide)
    place_assignee = models.OneToOneField(
        ParkingSpot,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.plaque_immat