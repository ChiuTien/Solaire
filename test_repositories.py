#!/usr/bin/env python3
"""
Test rapide pour les repositories ConfigJournee, Resultat et Statut
"""

from Database.Connexion import Connexion
from Models.ConfigJournee import ConfigJournee
from Models.Resultat import Resultat
from Models.Statut import Statut
from Repositories.ConfigJourneeRepository import ConfigJourneeRepository
from Repositories.ResultatRepository import ResultatRepository
from Repositories.StatutRepository import StatutRepository

# Connexion à la base de données
print("\n[CONNEXION] Établissement de la connexion...")
db_connexion = Connexion(
    serve="127.0.0.1,1433",
    db="Solaris",
    user="sa",
    password="MotDePasseFort123!"
)
db_connexion.connect()
connexion = db_connexion.connection

# Initialisation des repositories
statut_repo = StatutRepository(connexion)
config_repo = ConfigJourneeRepository(connexion)
resultat_repo = ResultatRepository(connexion)

print("=" * 60)
print("TEST STATUT REPOSITORY")
print("=" * 60)

# Test Statut - CREATE
print("\n[TEST SAVE] Création de 3 statuts...")
statut1 = Statut(None, "Actif")
statut2 = Statut(None, "Inactif")
statut3 = Statut(None, "En Maintenance")

statut_repo.save(statut1)
statut_repo.save(statut2)
statut_repo.save(statut3)

# Test Statut - COUNT
print(f"\n[TEST COUNT] Nombre total de statuts: {statut_repo.count()}")

# Test Statut - READ ALL
print("\n[TEST FINDALL] Tous les statuts:")
tous_les_statuts = statut_repo.findAll()
if tous_les_statuts:
    for statut in tous_les_statuts:
        print(f"  - ID: {statut[0]}, Nom: {statut[1]}")

# Test Statut - READ BY ID
print("\n[TEST FINDBYID] Récupération du statut ID 1:")
statut_trouve = statut_repo.findById(1)
if statut_trouve:
    print(f"  ✓ Trouvé: {statut_trouve}")
else:
    print(f"  ✗ Non trouvé")

# Test Statut - READ BY NOM
print("\n[TEST FINDBYNOM] Recherche du statut 'Actif':")
statut_by_nom = statut_repo.findByNom("Actif")
if statut_by_nom:
    print(f"  ✓ Trouvé: {statut_by_nom}")
else:
    print(f"  ✗ Non trouvé")

# Test Statut - UPDATE
print("\n[TEST UPDATE] Modification du statut ID 1:")
statut_repo.update(1, nom="Actif - Modifié")

print("\n" + "=" * 60)
print("TEST CONFIGJOURNEE REPOSITORY")
print("=" * 60)

# Test ConfigJournee - CREATE
print("\n[TEST SAVE] Création de 2 configurations de journée...")
config1 = ConfigJournee(None, "08:00", "12:00", 85, 1)
config2 = ConfigJournee(None, "12:00", "18:00", 75, 1)

config_repo.save(config1)
config_repo.save(config2)

# Test ConfigJournee - COUNT
print(f"\n[TEST COUNT] Nombre total de configurations: {config_repo.count()}")

# Test ConfigJournee - READ ALL
print("\n[TEST FINDALL] Toutes les configurations:")
toutes_les_configs = config_repo.findAll()
if toutes_les_configs:
    for config in toutes_les_configs:
        print(f"  - ID: {config[0]}, Début: {config[1]}, Fin: {config[2]}, Rendement: {config[3]}, Statut: {config[4]}")

# Test ConfigJournee - READ BY ID
print("\n[TEST FINDBYID] Récupération de la config ID 1:")
config_trouve = config_repo.findById(1)
if config_trouve:
    print(f"  ✓ Trouvé: {config_trouve}")
else:
    print(f"  ✗ Non trouvé")

# Test ConfigJournee - READ BY STATUT
print("\n[TEST FINDBYSTATUT] Configurations avec statut ID 1:")
configs_by_statut = config_repo.findByStatut(1)
if configs_by_statut:
    for config in configs_by_statut:
        print(f"  - ID: {config[0]}, Début: {config[1]}, Fin: {config[2]}")
else:
    print(f"  ✗ Aucune configuration trouvée")

# Test ConfigJournee - UPDATE
print("\n[TEST UPDATE] Modification de la config ID 1:")
config_repo.update(1, rendement=90)

print("\n" + "=" * 60)
print("TEST RESULTAT REPOSITORY")
print("=" * 60)

# Test Resultat - CREATE
print("\n[TEST SAVE] Création de 2 résultats...")
resultat1 = Resultat(None, 1, 1)
resultat2 = Resultat(None, 1, 2)

resultat_repo.save(resultat1)
resultat_repo.save(resultat2)

# Test Resultat - COUNT
print(f"\n[TEST COUNT] Nombre total de résultats: {resultat_repo.count()}")

# Test Resultat - READ ALL
print("\n[TEST FINDALL] Tous les résultats:")
tous_les_resultats = resultat_repo.findAll()
if tous_les_resultats:
    for resultat in tous_les_resultats:
        print(f"  - ID: {resultat[0]}, Config: {resultat[1]}, Ressource: {resultat[2]}")

# Test Resultat - READ BY ID
print("\n[TEST FINDBYID] Récupération du résultat ID 1:")
resultat_trouve = resultat_repo.findById(1)
if resultat_trouve:
    print(f"  ✓ Trouvé: {resultat_trouve}")
else:
    print(f"  ✗ Non trouvé")

# Test Resultat - READ BY CONFIG JOURNEE
print("\n[TEST FINDBYCONFIGJOURNEE] Résultats pour la config ID 1:")
resultats_by_config = resultat_repo.findByConfigJournee(1)
if resultats_by_config:
    for resultat in resultats_by_config:
        print(f"  - ID: {resultat[0]}, Config: {resultat[1]}, Ressource: {resultat[2]}")

# Test Resultat - READ BY RESSOURCE
print("\n[TEST FINDBYRESSOURCE] Résultats pour la ressource ID 1:")
resultats_by_ressource = resultat_repo.findByRessource(1)
if resultats_by_ressource:
    for resultat in resultats_by_ressource:
        print(f"  - ID: {resultat[0]}, Config: {resultat[1]}, Ressource: {resultat[2]}")

# Test Resultat - UPDATE
print("\n[TEST UPDATE] Modification du résultat ID 1:")
resultat_repo.update(1, idRessource=3)

print("\n" + "=" * 60)
print("TESTS COMPLÉTÉS")
print("=" * 60)

# Fermeture de la connexion
db_connexion.disconnect()
