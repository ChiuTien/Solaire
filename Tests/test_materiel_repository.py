"""
Script de test du MaterielRepository
Teste les opérations CRUD sur la table Materiel
"""

from Database.Connexion import Connexion
from Repositories.MaterielRepository import MaterielRepository
from Models.Materiel import Materiel

print("=" * 60)
print("TEST DU MATERIELREPOSITORY")
print("=" * 60)

# 1. Établir la connexion
print("\n[1] Établissement de la connexion...")
connexion = Connexion(
    serve="127.0.0.1,1433",
    db="Solaris",
    user="sa",
    password="MotDePasseFort123!"
)
connexion.connect()

# 2. Créer le repository
print("[2] Création du MaterielRepository...")
repo = MaterielRepository(connexion.connection)

# ===== CREATE / SAVE =====
print("\n" + "=" * 60)
print("TEST SAVE - Ajout de matériels")
print("=" * 60)

materiel1 = Materiel(nom="Laptop HP 15 pouces")
materiel2 = Materiel(nom="Souris optique USB")
materiel3 = Materiel(nom="Clavier Mécanique")
materiel4 = Materiel(nom="Moniteur")
materiel5 = Materiel(nom="Webcam")

print(f"\n[SAVE 1] Sauvegarde: {materiel1}")
repo.saveMateriel(materiel1)

print(f"[SAVE 2] Sauvegarde: {materiel2}")
repo.saveMateriel(materiel2)

print(f"[SAVE 3] Sauvegarde: {materiel3}")
repo.saveMateriel(materiel3)

print(f"[SAVE 4] Sauvegarde: {materiel4}")
repo.saveMateriel(materiel4)

print(f"[SAVE 5] Sauvegarde: {materiel5}")
repo.saveMateriel(materiel5)

# ===== READ =====
print("\n" + "=" * 60)
print("TEST READ - Vérification des données")
print("=" * 60)

print("\n[READ 1] Tous les matériels:")
tous = repo.findAll()
if tous:
    for row in tous:
        print(f"  ID: {row[0]}, Nom: {row[1]}")
else:
    print("  Aucun résultat")

print(f"\n[READ 2] Total: {repo.count()} matériels")

print("\n[READ 3] Rechercher par ID 1:")
materiel = repo.findById(1)
if materiel:
    print(f"  ID: {materiel[0]}, Nom: {materiel[1]}")
else:
    print("  Non trouvé")

print("\n[READ 4] Rechercher par nom contenant 'Laptop':")
resultats = repo.findByNom("Laptop")
if resultats:
    for row in resultats:
        print(f"  ID: {row[0]}, Nom: {row[1]}")
else:
    print("  Aucun résultat")

# ===== UPDATE =====
print("\n" + "=" * 60)
print("TEST UPDATE - Modification")
print("=" * 60)

print("\n[UPDATE 1] Modification du matériel 2:")
repo.update(2, nom="Souris Sans Fil Logitech")

print("[UPDATE 2] Vérification après modification:")
materiel = repo.findById(2)
if materiel:
    print(f"  ID: {materiel[0]}, Nom: {materiel[1]}")

# ===== DELETE =====
print("\n" + "=" * 60)
print("TEST DELETE - Suppression")
print("=" * 60)

print("\n[DELETE 1] Suppression du matériel 5:")
repo.delete(5)

print("[DELETE 2] Total après suppression:")
print(f"  {repo.count()} matériels restants")

print("\n[DELETE 3] Matériels restants:")
tous = repo.findAll()
if tous:
    for row in tous:
        print(f"  ID: {row[0]}, Nom: {row[1]}")

# ===== Fermer la connexion =====
print("\n" + "=" * 60)
print("FERMETURE DE LA CONNEXION")
print("=" * 60)
connexion.disconnect()

print("\n✓ Tests du MaterielRepository terminés!")
repo.saveMateriel(materiel1)

print(f"[SAVE 2] Sauvegarde: {materiel2}")
repo.saveMateriel(materiel2)

print(f"[SAVE 3] Sauvegarde: {materiel3}")
repo.saveMateriel(materiel3)

print(f"[SAVE 4] Sauvegarde: {materiel4}")
repo.saveMateriel(materiel4)

print(f"[SAVE 5] Sauvegarde: {materiel5}")
repo.saveMateriel(materiel5)

# ===== READ =====
print("\n" + "=" * 60)
print("TEST READ - Vérification des données")
print("=" * 60)

print("\n[READ 1] Tous les matériels:")
try:
    resultat = connexion.execute_query("SELECT * FROM Materiel")
    if resultat:
        for row in resultat:
            print(f"  {row}")
    else:
        print("  Aucun résultat")
except Exception as e:
    print(f"  Erreur: {e}")

# ===== BONUS TESTS =====
print("\n" + "=" * 60)
print("TESTS BONUS")
print("=" * 60)

print("\n[BONUS 1] Compter les matériels:")
try:
    resultat = connexion.execute_query("SELECT COUNT(*) as total FROM Materiel")
    if resultat:
        print(f"  Total: {resultat[0][0]} matériels")
except Exception as e:
    print(f"  Erreur: {e}")

print("\n[BONUS 2] Rechercher par nom 'Ordinateur':")
try:
    resultat = connexion.execute_query("SELECT * FROM Materiel WHERE nom LIKE '%Ordinateur%'")
    if resultat:
        for row in resultat:
            print(f"  {row}")
    else:
        print("  Aucun résultat")
except Exception as e:
    print(f"  Erreur: {e}")

# ===== Fermer la connexion =====
print("\n" + "=" * 60)
print("FERMETURE DE LA CONNEXION")
print("=" * 60)
connexion.disconnect()

print("\n✓ Tests du MaterielRepository terminés!")
