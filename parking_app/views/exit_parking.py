from django.shortcuts import render, redirect
from django.utils.timezone import now
from parking_app.models.ticket import Ticket
from parking_app.models.parking_spot import ParkingSpot

def exit_parking(request):
    if request.method == "POST":
        plate = request.POST.get("plate_number")

        try:
            ticket = Ticket.objects.get(vehicle__plate_number=plate)
        except Ticket.DoesNotExist:
            return render(request, "parking_app/exit_parking.html", {
                "error": "Aucun ticket trouvé pour cette plaque."
            })

        if ticket.exit_time:
            return render(request, "parking_app/exit_parking.html", {
                "error": "Ce véhicule est déjà sorti du parking."
            })

        # 1) Enregistre l’heure de sortie
        ticket.exit_time = now()

        # 2) Calcule le prix
        amount = ticket.compute_price()
        ticket.amount_paid = amount
        ticket.save()

        # 3) Libère la place
        spot = ticket.vehicle.assigned_spot
        if spot:
            spot.is_occupied = False
            spot.save()

            ticket.vehicle.assigned_spot = None
            ticket.vehicle.save()

        return render(request, "parking_app/exit_parking.html", {
            "success": f"Paiement effectué : {amount} €"
        })

    return render(request, "parking_app/exit_parking.html")
