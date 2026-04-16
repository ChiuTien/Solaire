#!/usr/bin/env python3
"""
Test de la fonction calculerCapaciteBatterieRequise
"""

from Database.Connexion import Connexion
from Models.Consommation import Consommation
from Repositories.ConsommationRepository import ConsommationRepository
from Services.ConsommationService import ConsommationService

# Connexion à la base de données
print("[CONNEXION] Établissement de la connexion...")
db_connexion = Connexion(
    serve="127.0.0.1,1433",
    db="Solaris",
    user="sa",
    password="MotDePasseFort123!"
)
db_connexion.connect()

# Créer le service
repo = ConsommationRepository(db_connexion.connection)
service = ConsommationService(repo)

print("\n" + "=" * 80)
print("TEST DE CALCUL DE CAPACITÉ DE BATTERIE")
print("=" * 80)

# Créer des consommations de test
print("\n[CRÉATION] Création de consommations de test...")
print("\nScénario: Deux appareils avec chevauchement horaire")

consommation1 = Consommation(
    id=None,
    idMateriel=1,
    puissance=70,       # 70 Watts
    heureDebut="22:00:00",
    heureFin="00:00:00" # Minuit (jour suivant)
)

consommation2 = Consommation(
    id=None,
    idMateriel=2,
    puissance=100,      # 100 Watts
    heureDebut="22:00:00",
    heureFin="23:00:00"
)

print("✓ Consommation 1: 70W de 22:00 à 00:00 (2 heures)")
print("✓ Consommation 2: 100W de 22:00 à 23:00 (1 heure)")

# Créer une liste de consommations
consommations = [consommation1, consommation2]

# Calculer la capacité requise
print("\n[CALCUL] Calcul de la capacité de batterie requise...\n")
resultat = service.calculerCapaciteBatterieRequise(consommations)

print("\n" + "=" * 80)
print("RÉSULTATS")
print("=" * 80)
print(f"\n✅ Détail du calcul:")
print(f"   Intervalle 22:00 → 23:00: (70W + 100W) × 1h = 170 Wh")
print(f"   Intervalle 23:00 → 00:00: 70W × 1h = 70 Wh")
print(f"   ─────────────────────────────────────────────")
print(f"   Capacité requise = 170 + 70 = 240 Wh\n")

print("=" * 80)
print("\n🔋 RECOMMANDATION:")
print(f"   Choisir une batterie avec une capacité minimum de {resultat['capacite_totale']:.0f} Wh")
print(f"   Capacité en kWh: {resultat['capacite_totale']/1000:.3f} kWh")

# Fermeture de la connexion
db_connexion.disconnect()

print("\n✓ Tests terminés!")
