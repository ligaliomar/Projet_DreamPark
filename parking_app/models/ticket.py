from django.db import models
from django.utils.timezone import now
from .vehicle import Vehicle

class Ticket(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    is_subscription = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ("cash", "Espèces"),
            ("cb", "Carte bancaire"),
        ]
    )

    exit_time = models.DateTimeField(null=True, blank=True)
    amount_paid = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.vehicle.plate_number}"

    # 👉 MÉTHODE À AJOUTER ICI
    def compute_price(self):
        """
        Calcule le prix total du parking 
        (2€/heure commencée).
        """
        if not self.exit_time:
            return None

        duration = self.exit_time - self.created_at
        hours = duration.total_seconds() / 3600

        # On arrondit à l'heure supérieure
        hours_ceiled = int(hours) + (1 if hours % 1 > 0 else 0)

        return hours_ceiled * 2  # 2€ par heure
