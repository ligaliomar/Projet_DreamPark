from django.db import models


class Abonne(models.Model):
    """
    Classe pour les abonnes du parking DreamPark
    Les abonnes peuvent beneficier de services speciaux comme dit dans le sujet
    """

    TYPES_ABONNEMENT = [
        ("STANDARD", "Abonné Standard"),
        ("GUARANTEED", "Pack Garanti"),
    ]

    # Infos personnelles de l'abonne
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    # Si l'abonnement est encore actif
    est_actif = models.BooleanField(default=True)
    # Date d'inscription
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        statut = 'actif' if self.est_actif else 'inactif'
        return f"{self.nom} ({statut})"
