#!/usr/bin/env python3
"""
Test de la fonction calculerPuissancePanneauRequise
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

print("\n" + "=" * 70)
print("TEST DE CALCUL DE PUISSANCE DU PANNEAU SOLAIRE")
print("=" * 70)

# Créer des consommations variées
print("\n[CRÉATION] Création de consommations de test...")

consommations = [
    Consommation(None, 1, 75, "09:00:00", "11:00:00"),   # 75W, 09:00-11:00
    Consommation(None, 2, 100, "10:30:00", "13:00:00"),  # 100W, 10:30-13:00
    Consommation(None, 3, 50, "13:00:00", "15:00:00"),   # 50W, 13:00-15:00
]

print("✓ Consommation 1: 75W de 09:00 à 11:00")
print("✓ Consommation 2: 100W de 10:30 à 13:00 (chevauchement!)")
print("✓ Consommation 3: 50W de 13:00 à 15:00")

# Test 1: Intervalle 10:00-14:00
print("\n\n📋 TEST 1: Panneau chargement de 10:00 à 14:00")
print("─" * 70)
print("Consommations actives lors de cet intervalle:")
print("  - C1 (75W) chevauche 10:00-11:00")
print("  - C2 (100W) chevauche 10:30-13:00")
print("  - C3 (50W) chevauche 13:00-14:00")
print()

resultat1 = service.calculerPuissancePanneauRequise(
    consommations,
    heureDebut="10:00:00",
    heureFin="14:00:00"
)

print(f"\n✅ Le panneau doit fournir au minimum {resultat1['puissance_max']:.2f}W")

# Test 2: Intervalle 11:00-13:00
print("\n\n📋 TEST 2: Panneau chargement de 11:00 à 13:00")
print("─" * 70)
print("Consommations actives lors de cet intervalle:")
print("  - C1 (75W) ne chevauchent PAS cet intervalle")
print("  - C2 (100W) chevauche 11:00-13:00")
print("  - C3 (50W) ne chevauchent PAS cet intervalle")
print()

resultat2 = service.calculerPuissancePanneauRequise(
    consommations,
    heureDebut="11:00:00",
    heureFin="13:00:00"
)

print(f"\n✅ Le panneau doit fournir au minimum {resultat2['puissance_max']:.2f}W")

# Test 3: Intervalle 13:00-14:00
print("\n\n📋 TEST 3: Panneau chargement de 13:00 à 14:00")
print("─" * 70)
print("Consommations actives lors de cet intervalle:")
print("  - C1 (75W) ne chevauchent PAS cet intervalle")
print("  - C2 (100W) ne chevauchent PAS cet intervalle")
print("  - C3 (50W) chevauche 13:00-14:00")
print()

resultat3 = service.calculerPuissancePanneauRequise(
    consommations,
    heureDebut="13:00:00",
    heureFin="14:00:00"
)

print(f"\n✅ Le panneau doit fournir au minimum {resultat3['puissance_max']:.2f}W")

# Résumé
print("\n\n" + "=" * 70)
print("RÉSUMÉ COMPARATIF")
print("=" * 70)
print("\n┌──────────────────────┬────────────────────┬─────────────────────┐")
print("│ Intervalle           │ Puissance max      │ Observation         │")
print("├──────────────────────┼────────────────────┼─────────────────────┤")
print(f"│ 10:00 → 14:00        │ {resultat1['puissance_max']:>16.2f}W │ Chevauchement max   │")
print(f"│ 11:00 → 13:00        │ {resultat2['puissance_max']:>16.2f}W │ Une seule console   │")
print(f"│ 13:00 → 14:00        │ {resultat3['puissance_max']:>16.2f}W │ Une seule console   │")
print("└──────────────────────┴────────────────────┴─────────────────────┘")

print("\n💡 Conclusion:")
print("   - Intervalle avec le plus de chevauchements = puissance max requise")
print("   - Le panneau doit pouvoir supporter le pic de 175W")
print("   - On voit bien l'impact des chevauchements!")

# Fermeture de la connexion
db_connexion.disconnect()

print("\n✓ Tests terminés!")
