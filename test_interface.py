#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier le fonctionnement de l'interface
et des calculs de dimensionnement solaire.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from Models.Consommation import Consommation
from Models.Materiel import Materiel
from Models.ConfigJournee import ConfigJournee
from Services.ConsommationService import ConsommationService
from config_exemple import (
    CONFIG_JOURNEE, CONFIG_BATTERIE, 
    APPAREILS_EXEMPLE_MAISON, APPAREILS_EXEMPLE_MINIMAL
)


class RepositoryStub:
    """Repository stub pour tests."""
    def save(self, obj):
        return True
    def findAll(self):
        return []
    def findById(self, id):
        return None


def test_exemple_minimal():
    """Test avec l'exemple minimal."""
    print("\n" + "="*70)
    print("🧪 TEST 1: Configuration MINIMALE")
    print("="*70)
    
    # Créer les matériels et consommations
    materiels = []
    consommations = []
    
    for idx, app in enumerate(APPAREILS_EXEMPLE_MINIMAL, 1):
        materiel = Materiel(nom=app['nom'])
        materiels.append(materiel)
        
        consommation = Consommation(
            id=idx,
            idMateriel=idx,
            puissance=app['consommation_w'],
            heureDebut=app['heure_debut'],
            heureFin=app['heure_fin']
        )
        consommations.append(consommation)
        print(f"✓ Appareil {idx}: {app['nom']} - {app['consommation_w']}W")
    
    # Créer les configurations
    config_matin = ConfigJournee(
        id=1,
        heureDebut=datetime.strptime(CONFIG_JOURNEE['matin']['heure_debut'], "%H:%M:%S").time(),
        heureFin=datetime.strptime(CONFIG_JOURNEE['matin']['heure_fin'], "%H:%M:%S").time(),
        rendement=CONFIG_JOURNEE['matin']['rendement'],
        idStatut=0
    )
    
    config_apres = ConfigJournee(
        id=2,
        heureDebut=datetime.strptime(CONFIG_JOURNEE['apres_midi']['heure_debut'], "%H:%M:%S").time(),
        heureFin=datetime.strptime(CONFIG_JOURNEE['apres_midi']['heure_fin'], "%H:%M:%S").time(),
        rendement=CONFIG_JOURNEE['apres_midi']['rendement'],
        idStatut=0
    )
    
    # Service
    service = ConsommationService(RepositoryStub())
    
    print("\n✓ Configuration chargée")
    print(f"  Matin: {CONFIG_JOURNEE['matin']['heure_debut']} → {CONFIG_JOURNEE['matin']['heure_fin']}")
    print(f"  Après-midi: {CONFIG_JOURNEE['apres_midi']['heure_debut']} → {CONFIG_JOURNEE['apres_midi']['heure_fin']}")
    print(f"  Batterie: {CONFIG_BATTERIE['capacite_wh']} Wh avec {CONFIG_BATTERIE['marge_securite']}% marge")
    
    # Calcul
    print("\n🧮 Lancement du calcul...")
    resultats = service.dimensionnerSystemeSolaire(
        consommations,
        config_matin,
        config_apres,
        CONFIG_BATTERIE['charge_debut'],
        CONFIG_BATTERIE['charge_fin'],
        CONFIG_BATTERIE['capacite_wh'],
        CONFIG_BATTERIE['marge_securite'] / 100
    )
    
    if resultats:
        print("\n✓ Calcul réussi!")
        print(f"\n📊 RÉSULTATS:")
        print(f"\n  🔋 Batterie:")
        print(f"     Puissance pratique: {resultats['batterie_puissance_pratique']:.2f}W")
        print(f"     Puissance théorique: {resultats['batterie_puissance_theorique']:.2f}W")
        print(f"\n  ☀️ Panneau:")
        print(f"     Puissance pratique: {resultats['puissance_pratique']:.2f}W")
        print(f"     Puissance théorique: {resultats['puissance_theorique']:.2f}W")
        return True
    else:
        print("\n✗ Erreur lors du calcul")
        return False


def test_exemple_maison():
    """Test avec l'exemple maison complète."""
    print("\n" + "="*70)
    print("🧪 TEST 2: Configuration MAISON COMPLÈTE")
    print("="*70)
    
    # Créer les matériels et consommations
    materiels = []
    consommations = []
    
    for idx, app in enumerate(APPAREILS_EXEMPLE_MAISON, 1):
        materiel = Materiel(nom=app['nom'])
        materiels.append(materiel)
        
        consommation = Consommation(
            id=idx,
            idMateriel=idx,
            puissance=app['consommation_w'],
            heureDebut=app['heure_debut'],
            heureFin=app['heure_fin']
        )
        consommations.append(consommation)
        print(f"✓ Appareil {idx}: {app['nom']} - {app['consommation_w']}W")
    
    # Créer les configurations
    config_matin = ConfigJournee(
        id=1,
        heureDebut=datetime.strptime(CONFIG_JOURNEE['matin']['heure_debut'], "%H:%M:%S").time(),
        heureFin=datetime.strptime(CONFIG_JOURNEE['matin']['heure_fin'], "%H:%M:%S").time(),
        rendement=CONFIG_JOURNEE['matin']['rendement'],
        idStatut=0
    )
    
    config_apres = ConfigJournee(
        id=2,
        heureDebut=datetime.strptime(CONFIG_JOURNEE['apres_midi']['heure_debut'], "%H:%M:%S").time(),
        heureFin=datetime.strptime(CONFIG_JOURNEE['apres_midi']['heure_fin'], "%H:%M:%S").time(),
        rendement=CONFIG_JOURNEE['apres_midi']['rendement'],
        idStatut=0
    )
    
    # Service
    service = ConsommationService(RepositoryStub())
    
    print("\n✓ Configuration chargée")
    print(f"  Matin: {CONFIG_JOURNEE['matin']['heure_debut']} → {CONFIG_JOURNEE['matin']['heure_fin']}")
    print(f"  Après-midi: {CONFIG_JOURNEE['apres_midi']['heure_debut']} → {CONFIG_JOURNEE['apres_midi']['heure_fin']}")
    print(f"  Batterie: {CONFIG_BATTERIE['capacite_wh']} Wh avec {CONFIG_BATTERIE['marge_securite']}% marge")
    
    # Calcul
    print("\n🧮 Lancement du calcul...")
    resultats = service.dimensionnerSystemeSolaire(
        consommations,
        config_matin,
        config_apres,
        CONFIG_BATTERIE['charge_debut'],
        CONFIG_BATTERIE['charge_fin'],
        CONFIG_BATTERIE['capacite_wh'],
        CONFIG_BATTERIE['marge_securite'] / 100
    )
    
    if resultats:
        print("\n✓ Calcul réussi!")
        print(f"\n📊 RÉSULTATS:")
        print(f"\n  🔋 Batterie:")
        print(f"     Puissance pratique: {resultats['batterie_puissance_pratique']:.2f}W")
        print(f"     Puissance théorique: {resultats['batterie_puissance_theorique']:.2f}W")
        print(f"\n  ☀️ Panneau:")
        print(f"     Puissance pratique: {resultats['puissance_pratique']:.2f}W")
        print(f"     Puissance théorique: {resultats['puissance_theorique']:.2f}W")
        return True
    else:
        print("\n✗ Erreur lors du calcul")
        return False


def main():
    """Lance tous les tests."""
    print("\n" + "🔋"*35)
    print("TESTS DE DIMENSIONNEMENT SOLAIRE")
    print("🔋"*35)
    
    results = []
    
    try:
        results.append(("Test minimal", test_exemple_minimal()))
    except Exception as e:
        print(f"\n✗ Erreur test minimal: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Test minimal", False))
    
    try:
        results.append(("Test maison", test_exemple_maison()))
    except Exception as e:
        print(f"\n✗ Erreur test maison: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Test maison", False))
    
    # Résumé
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*70)
    
    for test_name, result in results:
        status = "✓ SUCCÈS" if result else "✗ ÉCHEC"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✓ Tous les tests ont réussi!")
        print("\n💡 Vous pouvez maintenant utiliser l'interface GUI:")
        print("   python Interface.py")
    else:
        print("\n⚠️ Certains tests ont échoué. Consultez les erreurs ci-dessus.")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
