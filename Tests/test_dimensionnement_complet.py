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

# ============================================================
# TEST COMPLET: Dimensionnement du système solaire
# ============================================================

print("=" * 70)
print("TEST: DIMENSIONNEMENT COMPLET DU SYSTÈME SOLAIRE")
print("=" * 70)

# Créer un service
service = ConsommationService(None)

# Créer des consommations
consommations = [
    Consommation(id=1, idMateriel=1, puissance=75, heureDebut=time(10, 30), heureFin=time(11, 0)),
    Consommation(id=2, idMateriel=2, puissance=100, heureDebut=time(10, 0), heureFin=time(13, 0)),
    Consommation(id=3, idMateriel=3, puissance=50, heureDebut=time(13, 0), heureFin=time(14, 0))
]

# Créer un statut MATIN pour le jour
statut_matin = Statut(id=1, nom="matin")

# Créer une ConfigJournee pour le MATIN
# Matin: 06:00 à 12:00, rendement 40%
configJournee_matin = ConfigJournee(
    id=1,
    heureDebut=time(6, 0),
    heureFin=time(12, 0),
    rendement=40,
    idStatut=statut_matin.id
)

# Créer une ConfigJournee pour L'APRÈS-MIDI
# Après-midi: 12:00 à 18:00, rendement 20% (50% de 40%)
configJournee_apres = ConfigJournee(
    id=2,
    heureDebut=time(12, 0),
    heureFin=time(18, 0),
    rendement=20,
    idStatut=1  # Après-midi statut (on simule avec un autre id)
)

# Paramètres de charge batterie
heureChargeDebut = "10:00:00"
heureChargeFin = "14:00:00"
capaciteBatterie = 240  # Wh

print(f"\n📋 CONFIGURATION:")
print(f"  Batterie: {capaciteBatterie} Wh")
print(f"  Charge: {heureChargeDebut} → {heureChargeFin}")
print(f"  Matin: 06:00-12:00 (rendement 40%)")
print(f"  Après-midi: 12:00-18:00 (rendement 20%)")
print(f"  Appareils: 3 consommateurs")

# ============================================================
# APPEL DE LA FONCTION ORCHESTRATRICE
# ============================================================

resultat = service.dimensionnerSystemeSolaire(
    consommations,
    configJournee_matin,
    configJournee_apres,
    heureChargeDebut,
    heureChargeFin,
    capaciteBatterie,
    marge_batterie=0.50  # 50% de marge de sécurité
)

if resultat:
    print("\n" + "=" * 70)
    print("✅ RÉSULTATS FINAUX")
    print("=" * 70)
    
    print(f"\n🔋 BATTERIE:")
    print(f"  Capacité: {resultat['batterie_capacite']:.0f} Wh")
    print(f"  Puissance pratique: {resultat['batterie_puissance_pratique']:.2f}W")
    print(f"  Puissance théorique: {resultat['batterie_puissance_theorique']:.2f}W")
    print(f"  Marge de sécurité: {resultat['batterie_marge']*100:.0f}%")
    
    print(f"\n☀️  PANNEAU SOLAIRE:")
    print(f"  Puissance pratique: {resultat['puissance_pratique']:.2f}W")
    print(f"  Puissance théorique: {resultat['puissance_theorique']:.2f}W")
    print(f"  À acheter: Panneau de {resultat['puissance_theorique']:.2f}W")
    
    print(f"\n💡 RAISON DU DIMENSIONNEMENT:")
    print(f"  {resultat['logique']}")
    
    # Vérifications
    assert resultat['batterie_capacite'] == 240, "Capacité batterie incorrecte"
    assert resultat['rendement_matin'] == 40, "Rendement matin incorrect"
    print("\n✅ TOUS LES TESTS PASSENT!")
else:
    print("\n❌ Erreur dans le dimensionnement!")
