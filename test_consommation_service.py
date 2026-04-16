#!/usr/bin/env python3
"""
Test de la fonction calculerConsommationTotale
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

print("\n" + "=" * 60)
print("TEST DE CALCUL DE CONSOMMATION TOTALE")
print("=" * 60)

# Créer des consommations de test
print("\n[CRÉATION] Création de consommations de test...")

consommation1 = Consommation(
    id=None,
    idMateriel=1,
    puissance=75,      # 75 Watts (TV)
    heureDebut="19:00:00",
    heureFin="21:00:00"
)

consommation2 = Consommation(
    id=None,
    idMateriel=2,
    puissance=100,     # 100 Watts (Ordinateur)
    heureDebut="22:00:00",
    heureFin="23:00:00"
)

consommation3 = Consommation(
    id=None,
    idMateriel=3,
    puissance=200,     # 200 Watts (Réfrigérateur)
    heureDebut="00:00:00",
    heureFin="02:00:00"
)

print("✓ Consommation 1: TV 75W de 19:00 à 21:00 (2 heures)")
print("✓ Consommation 2: PC 100W de 22:00 à 23:00 (1 heure)")
print("✓ Consommation 3: Frigo 200W de 00:00 à 02:00 (2 heures)")

# Créer une liste de consommations
consommations = [consommation1, consommation2, consommation3]

# Calculer la consommation totale
print("\n[CALCUL] Calcul de la consommation totale...\n")
total_wh = service.calculerConsommationTotale(consommations)

print("\n" + "=" * 60)
print("RÉSULTATS")
print("=" * 60)
print(f"\nConsommation détaillée:")
print(f"  1. TV 75W × 2h = 150 Wh")
print(f"  2. PC 100W × 1h = 100 Wh")
print(f"  3. Frigo 200W × 2h = 400 Wh")
print(f"  ─────────────────────────")
print(f"  TOTAL = {total_wh:.2f} Wh = {total_wh/1000:.3f} kWh")

# Test avec liste vide
print("\n" + "=" * 60)
print("TEST AVEC LISTE VIDE")
print("=" * 60)
total_vide = service.calculerConsommationTotale([])

# Fermeture de la connexion
db_connexion.disconnect()

print("\n✓ Tests terminés!")
