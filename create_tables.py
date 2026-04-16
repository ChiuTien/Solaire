#!/usr/bin/env python3
"""Script pour créer les tables SQL"""

from Database.Connexion import Connexion
from sqlalchemy import text

db_connexion = Connexion(
    serve='127.0.0.1,1433',
    db='Solaris',
    user='sa',
    password='MotDePasseFort123!'
)
db_connexion.connect()

print("Création des tables...")

# Liste des instructions SQL à exécuter
sql_statements = [
    """CREATE TABLE Materiel (
        id INT PRIMARY KEY IDENTITY(1,1),
        nom NVARCHAR(100)
    )""",
    """CREATE TABLE Consommation (
        id INT PRIMARY KEY IDENTITY(1,1),
        idMateriel INT,
        puissance INT,
        heureDebut TIME,
        heureFin TIME
    )""",
    """CREATE TABLE Ressource (
        id INT PRIMARY KEY IDENTITY(1,1),
        nom NVARCHAR(100),
        puissanceTheorique DECIMAL(10,2),
        puissanceReelle DECIMAL(10,2)
    )""",
    """CREATE TABLE ConfigJournee (
        id INT PRIMARY KEY IDENTITY(1,1),
        heureDebut TIME,
        heureFin TIME,
        rendement INT,
        idStatut INT
    )""",
    """CREATE TABLE Resultat (
        id INT PRIMARY KEY IDENTITY(1,1),
        idConfigJournee INT,
        idRessource INT
    )""",
    """CREATE TABLE Statut (
        id INT PRIMARY KEY IDENTITY(1,1),
        nom VARCHAR(100)
    )"""
]

for statement in sql_statements:
    try:
        db_connexion.connection.execute(text(statement))
        db_connexion.connection.commit()
        # Extraire le nom de la table
        table_name = statement.split('TABLE')[1].strip().split('(')[0].strip()
        print(f'✓ Table créée: {table_name}')
    except Exception as e:
        error_msg = str(e)
        if 'already exists' in error_msg or 'Msg 2714' in error_msg or 'already' in error_msg.lower():
            table_name = statement.split('TABLE')[1].strip().split('(')[0].strip()
            print(f'ℹ Table déjà existante: {table_name}')
        else:
            print(f'✗ Erreur: {e}')

db_connexion.disconnect()
print('\n✓ Tables prêtes!')
