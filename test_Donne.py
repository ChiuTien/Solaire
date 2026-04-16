#!/usr/bin/env python3
"""Seed de donnees et tests du service de consommation pour Solaris."""

from math import isclose

from Database.Connexion import Connexion
from Models.ConfigJournee import ConfigJournee
from Models.Consommation import Consommation
from Models.Materiel import Materiel
from Models.Ressource import Ressource
from Models.Resultat import Resultat
from Models.Statut import Statut
from Repositories.ConfigJourneeRepository import ConfigJourneeRepository
from Repositories.ConsommationRepository import ConsommationRepository
from Repositories.MaterielRepository import MaterielRepository
from Repositories.RessourceRepository import RessourceRepository
from Repositories.ResultatRepository import ResultatRepository
from Repositories.StatutRepository import StatutRepository
from Services.ConsommationService import ConsommationService
from sqlalchemy import text


def reset_tables(connexion):
    """Vide les tables pour rendre le seed rejouable."""
    tables = [
        "Resultat",
        "ConfigJournee",
        "Consommation",
        "Ressource",
        "Materiel",
        "Statut",
    ]
    for table in tables:
        connexion.connection.execute(text(f"DELETE FROM {table}"))
    connexion.connection.commit()


def seed_data(connexion):
    """Insere les donnees de base dans la base Solaris."""
    materiel_repo = MaterielRepository(connexion)
    consommation_repo = ConsommationRepository(connexion)
    ressource_repo = RessourceRepository(connexion)
    statut_repo = StatutRepository(connexion)
    config_repo = ConfigJourneeRepository(connexion)
    resultat_repo = ResultatRepository(connexion)

    print("[INSERT] Creation des materiels...")
    materiel_repo.saveMateriel(Materiel("Panneau solaire"))
    materiel_repo.saveMateriel(Materiel("Batterie"))

    print("[INSERT] Creation des consommations...")
    consommation_repo.save(Consommation(None, 1, 6, "06:00:00", "19:00:00"))
    consommation_repo.save(Consommation(None, 1, 9, "19:00:00", "06:00:00"))
    consommation_repo.save(Consommation(None, 2, 2, "20:00:00", "08:00:00"))

    print("[INSERT] Creation des ressources...")
    ressource_repo.save(Ressource(None, "Panneau solaire", 100.0, 40.0))
    ressource_repo.save(Ressource(None, "Batterie", 100.0, 150.0))

    print("[INSERT] Creation des statuts...")
    statut_repo.save(Statut(None, "matin"))
    statut_repo.save(Statut(None, "midi"))
    statut_repo.save(Statut(None, "soir"))

    print("[INSERT] Creation des configurations de journee...")
    config_repo.save(ConfigJournee(None, "06:00:00", "19:00:00", 0.40, 1))
    config_repo.save(ConfigJournee(None, "19:00:00", "06:00:00", 0.50, 2))
    config_repo.save(ConfigJournee(None, "20:00:00", "08:00:00", 1.50, 3))

    print("[INSERT] Creation des resultats...")
    resultat_repo.save(Resultat(None, 1, 1))
    resultat_repo.save(Resultat(None, 2, 1))
    resultat_repo.save(Resultat(None, 3, 2))

    return {
        "materiel_repo": materiel_repo,
        "consommation_repo": consommation_repo,
        "ressource_repo": ressource_repo,
        "statut_repo": statut_repo,
        "config_repo": config_repo,
        "resultat_repo": resultat_repo,
    }


def charger_consommations(repo):
    """Convertit les lignes SQL en objets Consommation pour le service."""
    lignes = repo.findAll() or []
    return [Consommation(id_ligne[0], id_ligne[1], id_ligne[2], id_ligne[3], id_ligne[4]) for id_ligne in lignes]


def tester_calculs(service):
    """Execute des tests simples sur les fonctions de calcul du service."""
    consommations = [
        Consommation(None, 1, 10, "08:00:00", "12:00:00"),
        Consommation(None, 1, 20, "10:00:00", "13:00:00"),
        Consommation(None, 2, 15, "11:00:00", "14:00:00"),
    ]

    print("\n[TEST] calculerConsommationTotale")
    consommation_totale = service.calculerConsommationTotale(consommations)
    print(f"Resultat attendu: 145.0 Wh, obtenu: {consommation_totale:.2f} Wh")
    assert isclose(consommation_totale, 145.0, rel_tol=1e-9), "Consommation totale incorrecte"

    print("\n[TEST] calculerCapaciteBatterieRequise")
    batterie = service.calculerCapaciteBatterieRequise(consommations)
    capacite_totale = batterie["capacite_totale"]
    print(f"Resultat attendu: 145.0 Wh, obtenu: {capacite_totale:.2f} Wh")
    assert isclose(capacite_totale, 145.0, rel_tol=1e-9), "Capacite batterie incorrecte"

    print("\n[TEST] calculerPuissanceMaxSimultanee")
    puissance_max = service.calculerPuissanceMaxSimultanee(consommations)
    puissance_max_valeur = puissance_max["puissance_max"]
    print(f"Resultat attendu: 45 W, obtenu: {puissance_max_valeur} W")
    assert puissance_max_valeur == 45, "Puissance max simultanee incorrecte"

    print("\n[TEST] calculerPuissancePanneauRequise")
    panneau = service.calculerPuissancePanneauRequise(consommations, "09:00:00", "13:00:00")
    puissance_panneau = panneau["puissance_max"]
    print(f"Resultat attendu: 45 W, obtenu: {puissance_panneau} W")
    assert puissance_panneau == 45, "Puissance panneau requise incorrecte"

    print("\n[TEST] calculerPuissanceTotalePanneau")
    panneau_total = service.calculerPuissanceTotalePanneau(consommations, "09:00:00", "13:00:00", 5)
    puissance_totale = panneau_total["puissance_totale"]
    print(f"Resultat attendu: 50 W, obtenu: {puissance_totale} W")
    assert puissance_totale == 50, "Puissance totale panneau incorrecte"

    print("\n[OK] Tous les tests de calcul sont passes.")


def main():
    print("\n[CONNEXION] Etablissement de la connexion...")
    db_connexion = Connexion(
        serve="127.0.0.1,1433",
        db="Solaris",
        user="sa",
        password="MotDePasseFort123!",
    )
    db_connexion.connect()
    connexion = db_connexion.connection

    print("[RESET] Nettoyage des donnees existantes...")
    reset_tables(db_connexion)

    repositories = seed_data(connexion)
    consommation_service = ConsommationService(repositories["consommation_repo"])
    print("\n[RESUME]")
    print(f"  - Materiels: {repositories['materiel_repo'].count()}")
    print(f"  - Consommations: {repositories['consommation_repo'].count()}")
    print(f"  - Ressources: {repositories['ressource_repo'].count()}")
    print(f"  - Statuts: {repositories['statut_repo'].count()}")
    print(f"  - ConfigJournee: {repositories['config_repo'].count()}")
    print(f"  - Resultats: {repositories['resultat_repo'].count()}")

    tester_calculs(consommation_service)

    db_connexion.disconnect()


if __name__ == "__main__":
    main()