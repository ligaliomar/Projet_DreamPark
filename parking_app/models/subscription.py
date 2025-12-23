from django.db import models
from .abonne import Abonne


class Subscription(models.Model):
    """
    Represente un abonnement (contrat) pour un client abonne
    Il y a 2 types: Standard et Pack Garanti (voir sujet)
    """

    TYPES_FORMULES = [
        ("STANDARD", "Abonné Standard - 50€/mois"),
        ("GUARANTEED", "Pack Garanti - 100€/mois"),
    ]

    # L'abonne qui a souscrit
    abonne = models.ForeignKey(Abonne, on_delete=models.CASCADE, related_name="subscriptions")
    # Type de formule choisie
    type_formule = models.CharField(max_length=20, choices=TYPES_FORMULES)
    # Prix par mois
    prix_mensuel = models.FloatField()
    # Duree en mois (par defaut 12 mois = 1 an)
    duree_mois = models.IntegerField(default=12)
    # Dates de debut et fin du contrat
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField()
    # Si l'abonnement est toujours valide
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.abonne.nom} - {self.get_type_formule_display()}"

    class Meta:
        ordering = ['-date_debut']  # Les plus recents en premier
