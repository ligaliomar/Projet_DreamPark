from django.test import TestCase
from django.utils.timezone import now, timedelta
from parking_app.models import Vehicle, Ticket, ParkingSpot


class TicketModelTest(TestCase):
    """Tests unitaires pour le modèle Ticket."""

    def setUp(self):
        """Configuration initiale pour chaque test."""
        self.spot = ParkingSpot.objects.create(
            numero_place="A1",
            niveau=1,
            longueur_max=5.0,
            hauteur_max=2.5
        )
        self.vehicle = Vehicle.objects.create(
            plaque_immat="ABC123",
            longueur=4.0,
            hauteur=2.0,
            place_assignee=self.spot
        )

    def test_create_ticket(self):
        """Test de création d'un ticket."""
        ticket = Ticket.objects.create(
            vehicule=self.vehicle,
            a_un_abonnement=False,
            mode_paiement="cash"
        )
        self.assertEqual(ticket.vehicule, self.vehicle)
        self.assertFalse(ticket.a_un_abonnement)
        self.assertEqual(ticket.mode_paiement, "cash")
        self.assertIsNotNone(ticket.date_creation)
        self.assertIsNone(ticket.heure_sortie)
        self.assertIsNone(ticket.montant_paye)

    def test_ticket_str(self):
        """Test de la représentation string d'un ticket."""
        ticket = Ticket.objects.create(
            vehicule=self.vehicle,
            mode_paiement="cash"
        )
        expected = f"Ticket #{ticket.id} - ABC123"
        self.assertEqual(str(ticket), expected)

    def test_compute_price_one_hour(self):
        """Test du calcul de prix pour 1 heure."""
        ticket = Ticket.objects.create(
            vehicule=self.vehicle,
            mode_paiement="cash"
        )
        ticket.heure_sortie = ticket.date_creation + timedelta(hours=1)
        price = ticket.calculer_prix()
        self.assertEqual(price, 2)  # 2€/heure

    def test_compute_price_two_hours(self):
        """Test du calcul de prix pour 2 heures."""
        ticket = Ticket.objects.create(
            vehicule=self.vehicle,
            mode_paiement="cash"
        )
        ticket.heure_sortie = ticket.date_creation + timedelta(hours=2)
        price = ticket.calculer_prix()
        self.assertEqual(price, 4)  # 2€ × 2 heures

    def test_compute_price_partial_hour(self):
        """Test du calcul de prix pour heure partielle (arrondi supérieur)."""
        ticket = Ticket.objects.create(
            vehicule=self.vehicle,
            mode_paiement="cash"
        )
        ticket.heure_sortie = ticket.date_creation + timedelta(hours=1, minutes=30)
        price = ticket.calculer_prix()
        self.assertEqual(price, 4)  # Arrondi à 2 heures = 4€

    def test_compute_price_no_exit_time(self):
        """Test du calcul de prix sans heure de sortie."""
        ticket = Ticket.objects.create(
            vehicule=self.vehicle,
            mode_paiement="cash"
        )
        price = ticket.calculer_prix()
        self.assertIsNone(price)

    def test_payment_method_choices(self):
        """Test des méthodes de paiement disponibles."""
        ticket_cash = Ticket.objects.create(
            vehicule=self.vehicle,
            mode_paiement="cash"
        )
        self.assertEqual(ticket_cash.mode_paiement, "cash")

        # Créer nouveau véhicule pour éviter conflit OneToOne
        vehicle2 = Vehicle.objects.create(
            plaque_immat="DEF456",
            longueur=4.0,
            hauteur=2.0
        )
        ticket_cb = Ticket.objects.create(
            vehicule=vehicle2,
            mode_paiement="cb"
        )
        self.assertEqual(ticket_cb.mode_paiement, "cb")

    def test_ticket_with_subscription(self):
        """Test d'un ticket avec abonnement."""
        ticket = Ticket.objects.create(
            vehicule=self.vehicle,
            a_un_abonnement=True,
            mode_paiement="cb"
        )
        self.assertTrue(ticket.a_un_abonnement)
