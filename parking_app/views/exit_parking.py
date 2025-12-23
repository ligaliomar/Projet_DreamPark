from django.shortcuts import render, redirect
from django.utils.timezone import now
from parking_app.models.ticket import Ticket
from parking_app.models.parking_spot import ParkingSpot

def exit_parking(request):
    """
    Vue pour gerer la sortie d'un vehicule
    Le client presente son ticket et paye le montant
    """
    if request.method == "POST":
        # Recuperation de la plaque d'immat
        plaque = request.POST.get("plate_number")

        # Je cherche le ticket correspondant
        try:
            ticket = Ticket.objects.get(vehicule__plaque_immat=plaque)
        except Ticket.DoesNotExist:
            return render(request, "parking_app/exit_parking.html", {
                "error": "Aucun ticket trouve pour cette plaque."
            })

        # Verification que la voiture n'est pas deja sortie
        if ticket.heure_sortie:
            return render(request, "parking_app/exit_parking.html", {
                "error": "Ce vehicule a deja quitte le parking."
            })

        # 1) Enregistre l’heure de sortie
        ticket.heure_sortie = now()

        # 2) Calcule le prix
        amount = ticket.calculer_prix() or 0
        ticket.montant_paye = amount
        ticket.save()

        # 3) Libère la place
        spot = ticket.vehicule.place_assignee
        if spot:
            spot.est_occupee = False
            spot.save()

            ticket.vehicule.place_assignee = None
            ticket.vehicule.save()

        return render(request, "parking_app/exit_parking.html", {
            "success": f"Paiement effectué : {amount} €"
        })

    return render(request, "parking_app/exit_parking.html")
