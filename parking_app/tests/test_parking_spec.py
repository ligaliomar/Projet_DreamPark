from django.test import TestCase

class ParkingSpecificationTests(TestCase):

    def test_assign_place_when_available(self):
        """
        SPECIFICATION (Partie 0):
        - Si des places sont disponibles, le système doit renvoyer un identifiant de place.
        - La place doit être marquée comme occupée.
        - La voiture doit être enregistrée comme garée dans cette place.
        (Implémentation dans Partie 1)
        """
        self.assertTrue(True)  # placeholder pour la spécification

    def test_assign_place_when_full(self):
        """
        SPECIFICATION (Partie 0):
        - Si le parking est plein, le système renvoie une valeur spéciale (None ou -1).
        - Aucune place n'est modifiée.
        (Implémentation dans Partie 1)
        """
        self.assertTrue(True)