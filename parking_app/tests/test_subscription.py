from django.test import TestCase
from datetime import datetime, timedelta
from parking_app.models import Abonne, Subscription


class SubscriptionModelTest(TestCase):
    """Tests unitaires pour le modèle Subscription."""

    def setUp(self):
        """Configuration initiale pour chaque test."""
        self.abonne = Abonne.objects.create(
            nom="Test Abonné",
            email="test@example.com"
        )

    def test_create_subscription_standard(self):
        """Test de création d'un abonnement Standard."""
        date_fin = datetime.now() + timedelta(days=365)
        subscription = Subscription.objects.create(
            abonne=self.abonne,
            plan_type="STANDARD",
            prix_mensuel=50.0,
            duree_mois=12,
            date_fin=date_fin
        )
        self.assertEqual(subscription.abonne, self.abonne)
        self.assertEqual(subscription.plan_type, "STANDARD")
        self.assertEqual(subscription.prix_mensuel, 50.0)
        self.assertEqual(subscription.duree_mois, 12)
        self.assertTrue(subscription.is_active)

    def test_create_subscription_guaranteed(self):
        """Test de création d'un abonnement Pack Garanti."""
        date_fin = datetime.now() + timedelta(days=365)
        subscription = Subscription.objects.create(
            abonne=self.abonne,
            plan_type="GUARANTEED",
            prix_mensuel=100.0,
            duree_mois=12,
            date_fin=date_fin
        )
        self.assertEqual(subscription.plan_type, "GUARANTEED")
        self.assertEqual(subscription.prix_mensuel, 100.0)

    def test_subscription_str(self):
        """Test de la représentation string d'une subscription."""
        date_fin = datetime.now() + timedelta(days=365)
        subscription = Subscription.objects.create(
            abonne=self.abonne,
            plan_type="STANDARD",
            prix_mensuel=50.0,
            date_fin=date_fin
        )
        expected = "Test Abonné - Abonné Standard - 50€/mois"
        self.assertEqual(str(subscription), expected)

    def test_subscription_default_duree(self):
        """Test que la durée par défaut est 12 mois."""
        date_fin = datetime.now() + timedelta(days=365)
        subscription = Subscription.objects.create(
            abonne=self.abonne,
            plan_type="STANDARD",
            prix_mensuel=50.0,
            date_fin=date_fin
        )
        self.assertEqual(subscription.duree_mois, 12)

    def test_subscription_default_is_active(self):
        """Test que is_active est True par défaut."""
        date_fin = datetime.now() + timedelta(days=365)
        subscription = Subscription.objects.create(
            abonne=self.abonne,
            plan_type="STANDARD",
            prix_mensuel=50.0,
            date_fin=date_fin
        )
        self.assertTrue(subscription.is_active)

    def test_subscription_date_debut_auto(self):
        """Test que date_debut est automatiquement définie."""
        date_fin = datetime.now() + timedelta(days=365)
        subscription = Subscription.objects.create(
            abonne=self.abonne,
            plan_type="STANDARD",
            prix_mensuel=50.0,
            date_fin=date_fin
        )
        self.assertIsNotNone(subscription.date_debut)

    def test_multiple_subscriptions_per_abonne(self):
        """Test qu'un abonné peut avoir plusieurs subscriptions."""
        date_fin = datetime.now() + timedelta(days=365)
        sub1 = Subscription.objects.create(
            abonne=self.abonne,
            plan_type="STANDARD",
            prix_mensuel=50.0,
            date_fin=date_fin
        )
        sub2 = Subscription.objects.create(
            abonne=self.abonne,
            plan_type="GUARANTEED",
            prix_mensuel=100.0,
            date_fin=date_fin
        )
        self.assertEqual(self.abonne.subscriptions.count(), 2)

    def test_deactivate_subscription(self):
        """Test de la désactivation d'une subscription."""
        date_fin = datetime.now() + timedelta(days=365)
        subscription = Subscription.objects.create(
            abonne=self.abonne,
            plan_type="STANDARD",
            prix_mensuel=50.0,
            date_fin=date_fin
        )
        subscription.is_active = False
        subscription.save()
        subscription.refresh_from_db()
        self.assertFalse(subscription.is_active)
