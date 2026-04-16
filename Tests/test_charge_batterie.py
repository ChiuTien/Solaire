#!/usr/bin/env python3
"""
Test de la fonction calculerPuissanceNecessaire du ChargeBatterieService
"""

from Database.Connexion import Connexion
from Repositories.ChargeBatterieRepository import ChargeBatterieRepository
from Services.ChargeBatterieService import ChargeBatterieService

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
repo = ChargeBatterieRepository(db_connexion.connection)
service = ChargeBatterieService(repo)

print("\n" + "=" * 70)
print("TEST DE CALCUL DE PUISSANCE NÉCESSAIRE DU PANNEAU SOLAIRE")
print("=" * 70)

# Test 1: Charge sur 4 heures
print("\n\n📋 TEST 1: Charge de batterie 240Wh en 4 heures")
print("─" * 70)
resultat1 = service.calculerPuissanceNecessaire(
    heureDebut="10:00:00",
    heureFin="14:00:00",
    capaciteBatterie=240
)

print(f"\n  → Le panneau solaire doit fournir au minimum {resultat1['puissance_necessaire']:.2f}W")

# Test 2: Charge sur 8 heures
print("\n\n📋 TEST 2: Charge de batterie 240Wh en 8 heures")
print("─" * 70)
resultat2 = service.calculerPuissanceNecessaire(
    heureDebut="08:00:00",
    heureFin="16:00:00",
    capaciteBatterie=240
)

print(f"\n  → Le panneau solaire doit fournir au minimum {resultat2['puissance_necessaire']:.2f}W")

# Test 3: Charge sur 2 heures (très rapide)
print("\n\n📋 TEST 3: Charge de batterie 240Wh en 2 heures")
print("─" * 70)
resultat3 = service.calculerPuissanceNecessaire(
    heureDebut="12:00:00",
    heureFin="14:00:00",
    capaciteBatterie=240
)

print(f"\n  → Le panneau solaire doit fournir au minimum {resultat3['puissance_necessaire']:.2f}W")

# Test 4: Traverse minuit
print("\n\n📋 TEST 4: Charge de batterie 350Wh de 22:00 à 06:00 (8 heures)")
print("─" * 70)
resultat4 = service.calculerPuissanceNecessaire(
    heureDebut="22:00:00",
    heureFin="06:00:00",
    capaciteBatterie=350
)

print(f"\n  → Le panneau solaire doit fournir au minimum {resultat4['puissance_necessaire']:.2f}W")

# Résumé comparatif
print("\n\n" + "=" * 70)
print("RÉSUMÉ COMPARATIF")
print("=" * 70)
print("\n┌─────────────────┬──────────────────┬────────────────────────────┐")
print("│ Temps de charge │ Puissance requise│ Observations               │")
print("├─────────────────┼──────────────────┼────────────────────────────┤")
print(f"│ 4 heures        │ {resultat1['puissance_necessaire']:>14.2f}W │ Charge raisonnable         │")
print(f"│ 8 heures        │ {resultat2['puissance_necessaire']:>14.2f}W │ Charge lente               │")
print(f"│ 2 heures        │ {resultat3['puissance_necessaire']:>14.2f}W │ Charge rapide, panneaux +  │")
print(f"│ 8h (nuit traversée)│ {resultat4['puissance_necessaire']:>12.2f}W │ Charge très rapide à cause │")
print("└─────────────────┴──────────────────┴────────────────────────────┘")

print("\n💡 Conclusion:")
print("   - Plus le temps de charge est court, plus la puissance du panneau doit être élevée")
print("   - À l'inverse, une charge lente nécessite un panneau moins puissant")
print("   - C'est un trade-off entre coût du panneau et temps de charge")

# Fermeture de la connexion
db_connexion.disconnect()

print("\n✓ Tests terminés!")
