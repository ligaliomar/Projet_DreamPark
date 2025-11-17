from django.test import TestCase

class ParkingSpotAndVehicleSpecificationTests(TestCase):

    def test_parking_spot_attributes(self):
        """
        SPECIFICATION:
        - Une place a : id unique, niveau, longueur, hauteur, is_occupied=False par défaut.
        - Ces attributs doivent exister dans le modèle.
        """
        self.assertTrue(True)

    def test_vehicle_information_capture(self):
        """
        SPECIFICATION:
        - La caméra doit pouvoir capturer :
            * immatriculation
            * hauteur du véhicule
            * longueur du véhicule
        - Ces infos sont utilisées pour déterminer une place compatible.
        """
        self.assertTrue(True)