from django.db import models

class TracePassage(models.Model):
    """Stocke l'historique des entrées/sorties pour les statistiques"""
    immatriculation = models.CharField(max_length=20)
    date_entree = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField(null=True, blank=True)
    type_service = models.CharField(max_length=50, default='Aucun')

    def __str__(self):
        return f"{self.immatriculation} ({self.date_entree})"
