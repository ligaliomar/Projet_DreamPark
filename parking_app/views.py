from django.shortcuts import render
from .models import TracePassage  # Assurez-vous d'avoir créé ce modèle dans modèles.py

def statistiques_view(request):
    """
    Cette fonction est le 'Contrôleur'. 
    Elle calcule les données pour l'administrateur.
    """
    # 1. Récupérer les traces pour chaque voiture 
    traces = TracePassage.objects.all()
    
    # 2. Calculer la fréquentation (statistiques de base) [cite: 36]
    nombre_total = traces.count()
    
    # 3. Préparer les données pour la vue (HTML ou Texte) [cite: 39]
    context = {
        'total_vehicules': nombre_total,
        'historique_complet': traces,
    }
    
    return render(request, 'statistiques.html', context)
