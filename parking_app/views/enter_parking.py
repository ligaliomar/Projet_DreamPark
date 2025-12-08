from django.shortcuts import render
from django.http import HttpResponse
from parking_app.models import Vehicle
from parking_app.services.parking_manager import ParkingManager


def enter_parking_view(request):
    if request.method == "POST":

        # 1) Récupération des données
        plate = request.POST.get("plate_number")
        length_input = request.POST.get("length")
        height_input = request.POST.get("height")

        # 2) Vérifications - valeurs numériques
        try:
            length = float(length_input)
            height = float(height_input)
        except:
            return HttpResponse("❌ Dimensions invalides. Merci d'entrer des chiffres.", status=400)

        # 3) Vérifier que le véhicule n'est PAS déjà dans le parking
        if Vehicle.objects.filter(plate_number=plate, assigned_spot__isnull=False).exists():
            return HttpResponse("❌ Ce véhicule est déjà garé dans le parking.", status=400)

        # 4) Création du véhicule
        vehicle = Vehicle.objects.create(
            plate_number=plate,
            length=length,
            height=height,
        )

        # 5) Manager : assigner une place
        manager = ParkingManager()
        spot = manager.assign_place(vehicle)

        if spot is None:
            return HttpResponse("❌ Aucune place disponible.", status=400)

        # 6) Retour succès
        return HttpResponse(
            f"✔️ Place trouvée !<br>"
            f"Place : {spot.identifier} (Niveau {spot.level})<br>"
            f"Véhicule : {vehicle.plate_number}"
        )

    # Si GET → afficher formulaire
    return render(request, "parking_app/enter_parking.html")
