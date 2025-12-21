from django.test import TestCase
from .models import TracePassage

class StatistiquesTest(TestCase):
    def setUp(self):
        # On crée des données de test
        TracePassage.objects.create(immatriculation="AA-123-BB", type_service="LIVRAISON")
        TracePassage.objects.create(immatriculation="CC-456-DD", type_service="ENTRETIEN")

    def test_calcul_frequentation(self):
        """Vérifie que le nombre total de voitures est correct"""
        nb_voitures = TracePassage.objects.count()
        self.assertEqual(nb_voitures, 2)
