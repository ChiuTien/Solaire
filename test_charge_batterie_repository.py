"""
Script de test du ChargeBatterieRepository
Teste les operations CRUD sur la table ChargeBatterie
"""

from Database.Connexion import Connexion
from Models.ChargeBatterie import ChargeBatterie
from Repositories.ChargeBatterieRepository import ChargeBatterieRepository


print("=" * 60)
print("TEST DU CHARGEBATTERIEREPOSITORY")
print("=" * 60)

# 1. Etablir la connexion
print("\n[1] Etablissement de la connexion...")
connexion = Connexion(
    serve="127.0.0.1,1433",
    db="Solaris",
    user="sa",
    password="MotDePasseFort123!"
)
connexion.connect()

# 2. Creer le repository
print("[2] Creation du ChargeBatterieRepository...")
repo = ChargeBatterieRepository(connexion.connection)

# 3. SAVE
print("\n" + "=" * 60)
print("TEST SAVE")
print("=" * 60)

charge1 = ChargeBatterie("08:00", "10:00", 85.5, 12.2)
charge2 = ChargeBatterie("10:00", "12:00", 90.0, 10.7)

print(f"\n[SAVE 1] Sauvegarde: {charge1}")
repo.save(charge1)

print(f"[SAVE 2] Sauvegarde: {charge2}")
repo.save(charge2)

# 4. READ ALL
print("\n" + "=" * 60)
print("TEST FINDALL")
print("=" * 60)

toutes_les_charges = repo.findAll()
if toutes_les_charges:
    for row in toutes_les_charges:
        print(
            f"  ID: {row[0]}, Debut: {row[1]}, Fin: {row[2]}, "
            f"Capacite: {row[3]}, Puissance: {row[4]}"
        )
else:
    print("  Aucun resultat")

# 5. READ BY ID
print("\n" + "=" * 60)
print("TEST FINDBYID")
print("=" * 60)

charge = repo.findById(1)
if charge:
    print(
        f"  ID: {charge[0]}, Debut: {charge[1]}, Fin: {charge[2]}, "
        f"Capacite: {charge[3]}, Puissance: {charge[4]}"
    )
else:
    print("  Non trouve")

# 6. DELETE
print("\n" + "=" * 60)
print("TEST DELETE")
print("=" * 60)

print("\n[DELETE 1] Suppression de la charge ID 2")
repo.delete(2)

print("[DELETE 2] Verification des donnees restantes")
restantes = repo.findAll()
if restantes:
    for row in restantes:
        print(
            f"  ID: {row[0]}, Debut: {row[1]}, Fin: {row[2]}, "
            f"Capacite: {row[3]}, Puissance: {row[4]}"
        )

# 7. Fermer la connexion
print("\n" + "=" * 60)
print("FERMETURE DE LA CONNEXION")
print("=" * 60)
connexion.disconnect()

print("\nTests ChargeBatterieRepository termines")
