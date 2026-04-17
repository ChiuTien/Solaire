#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from datetime import time

# Ajouter les chemins PARENT (un niveau avant Tests/)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)  # Chemin parent pour tous les imports
sys.path.insert(0, os.path.join(parent_dir, 'Services'))
sys.path.insert(0, os.path.join(parent_dir, 'Models'))
sys.path.insert(0, os.path.join(parent_dir, 'Repositories'))
sys.path.insert(0, os.path.join(parent_dir, 'Database'))

from ConsommationService import ConsommationService
from Consommation import Consommation
from ConfigJournee import ConfigJournee
from Statut import Statut

print("=" * 70)
print("TEST: Appareil qui traverse 2 périodes (15:00 → 18:00)")
print("=" * 70)

service = ConsommationService(None)

# Appareil qui traverse matin et fin d'apres
consommations = [
    Consommation(id=1, idMateriel=1, puissance=100, heureDebut=time(15, 0), heureFin=time(18, 0))
]

print(f"\n📋 CONFIGURATION:")
print(f"  Appareil: 100W de 15:00 à 18:00")
print(f"  Batterie: 240 Wh")
print(f"  Charge: 10:00:00 → 14:00:00")
print(f"  P1 Matin:        06:00 → 17:00 (rendement 40%)")
print(f"  P2 Fin d'apres:  17:00 → 19:00 (rendement 20%)")

statut_matin = Statut(id=1, nom="matin")

configJournee_matin = ConfigJournee(
    id=1,
    heureDebut=time(6, 0),
    heureFin=time(17, 0),
    rendement=40,
    idStatut=statut_matin.id
)

configJournee_apres = ConfigJournee(
    id=2,
    heureDebut=time(17, 0),
    heureFin=time(19, 0),
    rendement=20,
    idStatut=1
)

resultat = service.dimensionnerSystemeSolaire(
    consommations,
    configJournee_matin,
    configJournee_apres,
    "10:00:00",
    "14:00:00",
    240,
    marge_batterie=0.50
)

if resultat:
    print("\n" + "=" * 70)
    print("✅ VÉRIFICATION")
    print("=" * 70)
    
    print(f"\n✓ Besoin matin: {resultat['besoins']['besoin_matin_pratique']:.2f}W")
    print(f"  (100W appareil [15:00-17:00] + 60W batterie [10:00-14:00])")
    print(f"  P1 doit couvrir le max: 100W appareil seul OU (100W[15-17] + 60W batterie[10-14]) = 160W")
    
    print(f"\n✓ Besoin après: {resultat['besoins']['besoin_apres_pratique']:.2f}W")
    print(f"  (100W appareil [17:00-18:00])")
    
    print(f"\n✓ Panneau pratique: {resultat['puissance_pratique']:.2f}W")
    print(f"✓ Panneau théorique: {resultat['puissance_theorique']:.2f}W")
    
else:
    print("\n❌ Erreur!")
