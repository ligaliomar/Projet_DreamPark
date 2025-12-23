from django.shortcuts import render
from django.db.models import Count, Sum, Q
from parking_app.models import Vehicle, Ticket, Subscription, ParkingSpot


def statistics_view(request):
    """Vue pour afficher les statistiques du parking DreamPark."""
    
    # === STATISTIQUES CLIENTS ===
    total_vehicles = Vehicle.objects.count()
    
    # Clients par type (via type_abonnement dans Vehicle)
    clients_occasionnels = Vehicle.objects.filter(
        type_abonnement=Vehicle.SubscriptionType.NONE
    ).count()
    
    clients_abonnes_standard = Vehicle.objects.filter(
        type_abonnement=Vehicle.SubscriptionType.STANDARD
    ).count()
    
    clients_pack_garanti = Vehicle.objects.filter(
        type_abonnement=Vehicle.SubscriptionType.GUARANTEED
    ).count()
    
    # === STATISTIQUES TICKETS ===
    total_tickets = Ticket.objects.count()
    
    # Tickets avec abonnement vs sans
    tickets_avec_abonnement = Ticket.objects.filter(
        abonnement__isnull=False
    ).count()
    
    tickets_sans_abonnement = Ticket.objects.filter(
        abonnement__isnull=True
    ).count()
    
    # === STATISTIQUES FINANCIÈRES ===
    # Revenus totaux (tickets payés)
    revenus_data = Ticket.objects.filter(
        montant_paye__isnull=False
    ).aggregate(
        total_revenus=Sum('montant_paye'),
        nb_paiements=Count('id')
    )
    
    total_revenus = revenus_data['total_revenus'] or 0
    nb_paiements = revenus_data['nb_paiements'] or 0
    
    # Revenus par type (occasionnels vs abonnés)
    revenus_occasionnels = Ticket.objects.filter(
        abonnement__isnull=True,
        montant_paye__isnull=False
    ).aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
    
    revenus_abonnes = Ticket.objects.filter(
        abonnement__isnull=False,
        montant_paye__isnull=False
    ).aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
    
    # === STATISTIQUES PLACES ===
    total_places = ParkingSpot.objects.count()
    places_occupees = ParkingSpot.objects.filter(est_occupee=True).count()
    places_disponibles = ParkingSpot.objects.filter(est_occupee=False).count()
    
    taux_occupation = 0
    if total_places > 0:
        taux_occupation = round((places_occupees / total_places) * 100, 1)
    
    # === STATISTIQUES ABONNEMENTS ===
    total_subscriptions = Subscription.objects.count()
    subscriptions_actives = Subscription.objects.filter(est_actif=True).count()
    
    # Par type de plan
    plans_stats = Subscription.objects.values('type_formule').annotate(
        count=Count('id')
    )
    
    plans_data = {}
    for plan in plans_stats:
        plans_data[plan['type_formule']] = plan['count']
    
    # === CONTEXTE POUR LE TEMPLATE ===
    context = {
        # Clients
        'total_vehicles': total_vehicles,
        'clients_occasionnels': clients_occasionnels,
        'clients_abonnes_standard': clients_abonnes_standard,
        'clients_pack_garanti': clients_pack_garanti,
        
        # Tickets
        'total_tickets': total_tickets,
        'tickets_avec_abonnement': tickets_avec_abonnement,
        'tickets_sans_abonnement': tickets_sans_abonnement,
        
        # Finances
        'total_revenus': total_revenus,
        'nb_paiements': nb_paiements,
        'revenus_occasionnels': revenus_occasionnels,
        'revenus_abonnes': revenus_abonnes,
        
        # Places
        'total_places': total_places,
        'places_occupees': places_occupees,
        'places_disponibles': places_disponibles,
        'taux_occupation': taux_occupation,
        
        # Subscriptions
        'total_subscriptions': total_subscriptions,
        'subscriptions_actives': subscriptions_actives,
        'plans_data': plans_data,
    }
    
    return render(request, 'parking_app/statistics.html', context)
