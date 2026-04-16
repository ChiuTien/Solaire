#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from datetime import time

# Ajouter le chemin des Services
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Services'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Models'))

from ConsommationService import ConsommationService
from ChargeBatterieService import ChargeBatterieService
from Consommation import Consommation

# ============================================================
# TESTS: Puissance totale panneau (appareils + batterie)
# ============================================================

print("=" * 70)
print("TESTS: Puissance totale requise du panneau solaire")
print("=" * 70)

# ConsommationService n'a besoin du repo que pour persistence, pas pour les calculs
service = ConsommationService(None)

# Test 1: Batterie de 240Wh + appareils consommant lors de la charge
print("\n[Test 1] Charge batterie 10:00-14:00 (4h) avec appareils actifs")
print("-" * 70)

consommations_test1 = [
    Consommation(
        id=1,
        idMateriel=1,
        puissance=75,
        heureDebut=time(10, 30),
        heureFin=time(11, 0)
    ),
    Consommation(
        id=2,
        idMateriel=2,
        puissance=100,
        heureDebut=time(10, 0),
        heureFin=time(13, 0)
    ),
    Consommation(
        id=3,
        idMateriel=3,
        puissance=50,
        heureDebut=time(13, 0),
        heureFin=time(14, 0)
    )
]

# Calcul de la puissance de charge batterie
# Batterie: 240Wh, charger en 4h → 60W
resultat_charge = ChargeBatterieService(None).calculerPuissanceNecessaire(
    "10:00:00", "14:00:00", 240
)
puissance_charge = resultat_charge['puissance_necessaire']

print(f"\nCapacité batterie: 240Wh")
print(f"Fenêtre charge: 10:00 → 14:00 (4 heures)")
print(f"Puissance charge batterie: {puissance_charge:.2f}W")

# Calcul de la puissance totale avec rendement 100% (optimal)
resultat_total = service.calculerPuissanceTotalePanneau(
    consommations_test1,
    "10:00:00",
    "14:00:00",
    puissance_charge,
    rendement=100
)

assert resultat_total['puissance_appareils'] == 175, f"Attendu 175W, reçu {resultat_total['puissance_appareils']}"
assert resultat_total['puissance_batterie'] == puissance_charge, "Puissance batterie ne correspond pas"
assert resultat_total['puissance_requise'] == 175 + puissance_charge, "Puissance requise ne correspond pas"
print(f"✅ Test 1a réussi (rendement 100%): {resultat_total['puissance_theorique']:.0f}W")

# Même test MAIS avec rendement 80% (soleil moins intense)
print("\n[Test 1b] Même calcul mais avec rendement 80% (soleil moins intense)")
print("-" * 70)

resultat_total_80 = service.calculerPuissanceTotalePanneau(
    consommations_test1,
    "10:00:00",
    "14:00:00",
    puissance_charge,
    rendement=80
)

assert resultat_total_80['puissance_appareils'] == 175
assert resultat_total_80['puissance_batterie'] == puissance_charge
assert resultat_total_80['puissance_requise'] == 175 + puissance_charge
# 235W / 0.80 = 293.75W
assert abs(resultat_total_80['puissance_theorique'] - 293.75) < 0.01, "Calcul du rendement incorrect"
print(f"✅ Test 1b réussi (rendement 80%): {resultat_total_80['puissance_theorique']:.2f}W")

# Test 2: Même batterie, mais fenêtre de charge de 8h
print("\n\n[Test 2] Charge batterie 06:00-14:00 (8h) avec appareils actifs")
print("-" * 70)

resultat_charge_8h = ChargeBatterieService(None).calculerPuissanceNecessaire(
    "06:00:00", "14:00:00", 240
)
puissance_charge_8h = resultat_charge_8h['puissance_necessaire']

print(f"\nCapacité batterie: 240Wh")
print(f"Fenêtre charge: 06:00 → 14:00 (8 heures)")
print(f"Puissance charge batterie: {puissance_charge_8h:.2f}W")

resultat_total_8h = service.calculerPuissanceTotalePanneau(
    consommations_test1,
    "06:00:00",
    "14:00:00",
    puissance_charge_8h,
    rendement=85
)

assert resultat_total_8h['puissance_appareils'] == 175
assert resultat_total_8h['puissance_batterie'] == puissance_charge_8h
# 205W / 0.85 = 241.18W
assert abs(resultat_total_8h['puissance_theorique'] - (175 + puissance_charge_8h) / 0.85) < 0.01
print(f"✅ Test 2 réussi (rendement 85%): {resultat_total_8h['puissance_theorique']:.2f}W")

# Test 3: Fenêtre de charge sans aucun appareil actif
print("\n\n[Test 3] Charge batterie 22:00-02:00 (4h) SANS appareils actifs")
print("-" * 70)

resultat_charge_nuit = ChargeBatterieService(None).calculerPuissanceNecessaire(
    "22:00:00", "02:00:00", 240
)
puissance_charge_nuit = resultat_charge_nuit['puissance_necessaire']

print(f"\nCapacité batterie: 240Wh")
print(f"Fenêtre charge: 22:00 → 02:00 (4 heures) [dépasse minuit]")
print(f"Puissance charge batterie: {puissance_charge_nuit:.2f}W")

resultat_total_nuit = service.calculerPuissanceTotalePanneau(
    consommations_test1,  # Consommations le jour
    "22:00:00",
    "02:00:00",
    puissance_charge_nuit,
    rendement=50  # La nuit, rendement très faible!
)

# Aucun appareil actif de 22:00 à 02:00
assert resultat_total_nuit['puissance_appareils'] == 0, f"Attendu 0W appareils, reçu {resultat_total_nuit['puissance_appareils']}"
assert resultat_total_nuit['puissance_batterie'] == puissance_charge_nuit
# 60W / 0.50 = 120W
assert abs(resultat_total_nuit['puissance_theorique'] - (puissance_charge_nuit / 0.50)) < 0.01
print(f"✅ Test 3 réussi (rendement 50%): Panneau doit théoriquement fournir {resultat_total_nuit['puissance_theorique']:.2f}W")

print("\n" + "=" * 70)
print("✅ TOUS LES TESTS RÉUSSIS!")
print("=" * 70)
print("\nRÉSUMÉ:")
print(f"  Test 1a (rendement 100%) : {resultat_total['puissance_theorique']:.0f}W théorique (235W requise)")
print(f"  Test 1b (rendement 80%)  : {resultat_total_80['puissance_theorique']:.2f}W théorique (235W requise)")
print(f"  Test 2  (rendement 85%)  : {resultat_total_8h['puissance_theorique']:.2f}W théorique")
print(f"  Test 3  (rendement 50%)  : {resultat_total_nuit['puissance_theorique']:.2f}W théorique (60W requise)")
print("\n💡 OBSERVATION:")
print("  Plus le rendement est faible (mauvaises conditions solaires),")
print("  plus le panneau doit théoriquement fournir de puissance!")
print(f"  Exemple Test 1: 235W requise → 235W à 100% vs 293.75W à 80%")
