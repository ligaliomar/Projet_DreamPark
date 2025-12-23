from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from parking_app.models import Vehicle, Subscription, Abonne
from parking_app.services.parking_manager import ParkingManager


def enter_parking_view(request):
    """
    Vue pour gerer l'entree d'un vehicule dans le parking
    C'est ici qu'on recupere les infos de la voiture et qu'on lui trouve une place
    """
    if request.method == "POST":

        # Recup des infos du vehicule depuis le formulaire
        plaque = request.POST.get("plate_number")
        longueur_saisie = request.POST.get("length")
        hauteur_saisie = request.POST.get("height")
        
        # Est-ce que c'est un abonne?
        a_abonnement = request.POST.get("has_subscription") == "on"
        nom_abonne = request.POST.get("abonne_nom")
        email_abonne = request.POST.get("abonne_email")
        type_formule = request.POST.get("plan_type")  # "STANDARD" ou "GUARANTEED"

        # Verification que les dimensions sont bien des nombres
        try:
            longueur = float(longueur_saisie)
            hauteur = float(hauteur_saisie)
        except:
            return HttpResponse("❌ Les dimensions doivent etre des nombres!", status=400)

        # Verifier que la voiture n'est pas deja dans le parking
        if Vehicle.objects.filter(plaque_immat=plaque, place_assignee__isnull=False).exists():
            return HttpResponse("❌ Cette voiture est déjà garée ici.", status=400)

        # Gestion de l'abonnement si le client en a un
        abonnement = None
        type_abon = Vehicle.SubscriptionType.NONE
        
        if a_abonnement:
            if not nom_abonne or not email_abonne or not type_formule:
                return HttpResponse("❌ Il faut remplir tous les champs pour l'abonnement.", status=400)
            
            try:
                # Creation de l'abonne dans la base
                client_abonne = Abonne.objects.create(
                    nom=nom_abonne,
                    email=email_abonne
                )
                
                # Creation du contrat d'abonnement (1 an)
                date_expiration = datetime.now() + timedelta(days=365)
                abonnement = Subscription.objects.create(
                    abonne=client_abonne,
                    type_formule=type_formule,
                    prix_mensuel=50 if type_formule == "STANDARD" else 100,
                    duree_mois=12,
                    date_fin=date_expiration,
                    est_actif=True
                )
                
                # Je determine le type d'abonnement pour le vehicule
                if type_formule == "STANDARD":
                    type_abon = Vehicle.SubscriptionType.STANDARD
                elif type_formule == "GUARANTEED":
                    type_abon = Vehicle.SubscriptionType.GUARANTEED
                    
            except Exception as erreur:
                return HttpResponse(f"❌ Probleme avec l'abonnement : {str(erreur)}", status=400)

        # Creation du vehicule dans la BDD
        voiture = Vehicle.objects.create(
            plaque_immat=plaque,
            longueur=longueur,
            hauteur=hauteur,
            type_abonnement=type_abon
        )

        # J'utilise le manager pour trouver une place
        gestionnaire = ParkingManager()
        place_trouvee = gestionnaire.attribuer_place(voiture, abonnement=abonnement)

        # Si y'a pas de place disponible
        if place_trouvee is None:
            return HttpResponse("❌ Désolé, le parking est complet.", status=400)

        # Tout est bon, on retourne un message de succes
        return HttpResponse(
            f"✔️ Plac e attribuée : {place_trouvee.numero_place} (niveau {place_trouvee.niveau})<br>"
            f"Type client : {type_abon}<br>"
            f"Immatriculation : {plaque}"
        )


    # Si c'est un GET, on affiche juste le formulaire
    return render(request, "parking_app/enter_parking.html")
