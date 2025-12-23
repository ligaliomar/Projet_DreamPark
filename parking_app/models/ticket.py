from django.db import models
from django.utils.timezone import now
from .vehicle import Vehicle
from .subscription import Subscription


class Ticket(models.Model):
    """
    Ticket delivre quand un vehicule entre dans le parking
    Comme dans le sujet, la borne delivre un ticket
    """
    vehicule = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    abonnement = models.ForeignKey(
        Subscription,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tickets"
    )
    # Date et heure de creation du ticket
    date_creation = models.DateTimeField(auto_now_add=True)

    # Si le client a un abonnement ou pas
    a_un_abonnement = models.BooleanField(default=False)
    # Mode de paiement choisi (espece ou CB)
    mode_paiement = models.CharField(
        max_length=20,
        choices=[
            ("cash", "Espèces"),
            ("cb", "Carte bancaire"),
        ]
    )

    # Heure de sortie (vide tant que la voiture est encore la)
    heure_sortie = models.DateTimeField(null=True, blank=True)
    # Montant paye a la sortie
    montant_paye = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.vehicule.plaque_immat}"

    def calculer_prix(self):
        """
        Calcule le prix a payer pour le parking
        Tarif: 2 euros par heure commencee
        """
        # Si pas encore sorti, on peut pas calculer
        if not self.heure_sortie:
            return None

        # Calcul de la duree de stationnement
        duree = self.heure_sortie - self.date_creation
        nb_heures = duree.total_seconds() / 3600

        # Arrondi a l'heure superieure (meme 10min = 1h payee)
        heures_a_payer = int(nb_heures)
        if nb_heures % 1 > 0:  # S'il reste des minutes
            heures_a_payer += 1

        prix_total = heures_a_payer * 2  # 2 euros l'heure
        return prix_total
