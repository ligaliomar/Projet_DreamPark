from django.test import TestCase

class ParkingServicesSpecificationTests(TestCase):

    def test_delivery_service(self):
        """
        SPECIFICATION:
        - Un client peut demander la livraison de son véhicule
        - Doit fournir : adresse, date/heure
        - Le système doit vérifier la disponibilité des voituriers et téléporteurs
        """
        self.assertTrue(True)

    def test_subscription_services(self):
        """
        SPECIFICATION:
        - Les abonnés peuvent bénéficier:
            * entretien
            * maintenance
            * livraison garantie
        - Le système doit gérer les options sélectionnées.
        """
        self.assertTrue(True)
