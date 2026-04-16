#!/usr/bin/env python3
"""
Validation par le code des fonctions de ConsommationService:
- calculerCapaciteBatterieRequise
- calculerPuissanceMaxSimultanee
- calculerConsommationTotale

Ce script utilise MaterielService et ConsommationService avec des repositories
en memoire (pas de base SQL necessaire) pour prouver les resultats.
"""

from math import isclose

from Models.Consommation import Consommation
from Models.Materiel import Materiel
from Services.ConsommationService import ConsommationService
from Services.MaterielService import MaterielService


class InMemoryMaterielRepository:
    """Repository materiel minimal en memoire pour les tests."""

    def __init__(self):
        self._rows = []
        self._next_id = 1

    def saveMateriel(self, materiel):
        materiel.id = self._next_id
        self._next_id += 1
        self._rows.append((materiel.id, materiel.nom))
        return True

    def findAll(self):
        return list(self._rows)

    def findById(self, id_materiel):
        for row in self._rows:
            if row[0] == id_materiel:
                return row
        return None

    def findByNom(self, nom):
        return [row for row in self._rows if nom.lower() in row[1].lower()]

    def update(self, id_materiel, nom=None):
        for i, row in enumerate(self._rows):
            if row[0] == id_materiel:
                self._rows[i] = (id_materiel, nom or row[1])
                return True
        return False

    def delete(self, id_materiel):
        for i, row in enumerate(self._rows):
            if row[0] == id_materiel:
                del self._rows[i]
                return True
        return False

    def count(self):
        return len(self._rows)


class DummyConsommationRepository:
    """Stub pour instancier ConsommationService sans DB."""

    def save(self, consommation):
        return True

    def findAll(self):
        return []

    def findById(self, id_consommation):
        return None

    def findByMateriel(self, idMateriel):
        return []

    def update(self, id_consommation, idMateriel=None, puissance=None, heureDebut=None, heureFin=None):
        return True

    def delete(self, id_consommation):
        return True

    def count(self):
        return 0


def build_services_with_materiels():
    """Cree MaterielService + ConsommationService et ajoute des materiels de test."""
    materiel_service = MaterielService(InMemoryMaterielRepository())
    consommation_service = ConsommationService(DummyConsommationRepository())

    noms = [
        "TV",
        "Phone",
        "PC",
        "Frigo",
        "Routeur",
        "Pompe",
        "Lampe",
    ]
    for nom in noms:
        materiel_service.saveMateriel(Materiel(nom=nom))

    return materiel_service, consommation_service


def run_case_capacite(consommation_service, case_name, consommations, expected_total_wh):
    result = consommation_service.calculerCapaciteBatterieRequise(consommations)
    ok = isclose(result["capacite_totale"], expected_total_wh, rel_tol=1e-9, abs_tol=1e-6)
    if not ok:
        raise AssertionError(
            f"[{case_name}] capacite_totale attendue={expected_total_wh}, obtenue={result['capacite_totale']}"
        )
    print(f"PASS capacite: {case_name} -> {result['capacite_totale']:.2f} Wh")


def run_case_puissance_max(consommation_service, case_name, consommations, expected_max):
    result = consommation_service.calculerPuissanceMaxSimultanee(consommations)
    ok = isclose(result["puissance_max"], expected_max, rel_tol=1e-9, abs_tol=1e-6)
    if not ok:
        raise AssertionError(
            f"[{case_name}] puissance_max attendue={expected_max}, obtenue={result['puissance_max']}"
        )
    print(f"PASS puissance max: {case_name} -> {result['puissance_max']:.2f} W")


def run_case_conso_totale(consommation_service, case_name, consommations, expected_wh):
    result = consommation_service.calculerConsommationTotale(consommations)
    ok = isclose(result, expected_wh, rel_tol=1e-9, abs_tol=1e-6)
    if not ok:
        raise AssertionError(
            f"[{case_name}] consommation_totale attendue={expected_wh}, obtenue={result}"
        )
    print(f"PASS conso totale: {case_name} -> {result:.2f} Wh")


def get_test_data_calculer_capacite_batterie():
    """
    Retourne des jeux de donnees de test prets a utiliser.

    Chaque scenario contient:
    - name: nom du cas
    - description: explication
    - consommations: liste d'objets Consommation
    """
    scenarios = []

    # Cas 1: donnee PM simple -> 120W * 1.5h = 180Wh
    scenarios.append({
        "name": "cas_pm_simple",
        "description": "Consommation simple en PM.",
        "consommations": [
            Consommation(id=None, idMateriel=1, puissance=120, heureDebut="20:30:00", heureFin="22:00:00"),
        ],
        "expected": {
            "capacite_totale_wh": 180.0
        }
    })

    # Cas 2: chevauchement classique
    # 06-07:100 + 07-08:145 + 08-09:95 + 09-10:50 = 390Wh
    scenarios.append({
        "name": "chevauchement_max",
        "description": "Chevauchements multiples.",
        "consommations": [
            Consommation(id=None, idMateriel=1, puissance=100, heureDebut="06:00:00", heureFin="08:00:00"),
            Consommation(id=None, idMateriel=2, puissance=45, heureDebut="07:00:00", heureFin="09:00:00"),
            Consommation(id=None, idMateriel=1, puissance=50, heureDebut="07:00:00", heureFin="10:00:00"),
        ],
        "expected": {
            "capacite_totale_wh": 390.0
        }
    })

    # Cas 3: traverser minuit
    # 22:00-23:30:70W (1.5h=105Wh)
    # 23:30-01:30:110W (2h=220Wh)
    # 01:30-04:00:40W (2.5h=100Wh)
    # Total=425Wh
    scenarios.append({
        "name": "traverse_minuit",
        "description": "Charge qui traverse minuit avec chevauchement.",
        "consommations": [
            Consommation(id=None, idMateriel=6, puissance=70, heureDebut="22:00:00", heureFin="01:30:00"),
            Consommation(id=None, idMateriel=7, puissance=40, heureDebut="23:30:00", heureFin="04:00:00"),
        ],
        "expected": {
            "capacite_totale_wh": 425.0
        }
    })

    # Cas 4: donnees vides
    scenarios.append({
        "name": "vide",
        "description": "Aucune consommation.",
        "consommations": [],
        "expected": {
            "capacite_totale_wh": 0.0
        }
    })

    return scenarios


def get_test_data_puissance_max_simultanee():
    """
    Jeux de donnees pour calculerPuissanceMaxSimultanee.

    Les champs expected servent de repere pour verifier rapidement le resultat.
    """
    scenarios = []

    scenarios.append({
        "name": "simple_sans_chevauchement",
        "description": "Consommations successives, puissance max = plus grande charge unique.",
        "consommations": [
            Consommation(id=None, idMateriel=21, puissance=60, heureDebut="08:00:00", heureFin="09:00:00"),
            Consommation(id=None, idMateriel=22, puissance=90, heureDebut="09:00:00", heureFin="10:00:00"),
        ],
        "expected": {
            "puissance_max": 90
        }
    })

    scenarios.append({
        "name": "chevauchement_fort",
        "description": "Chevauchement de plusieurs charges pour observer le pic de puissance.",
        "consommations": [
            Consommation(id=None, idMateriel=23, puissance=100, heureDebut="06:00:00", heureFin="08:00:00"),
            Consommation(id=None, idMateriel=24, puissance=45, heureDebut="07:00:00", heureFin="09:00:00"),
            Consommation(id=None, idMateriel=25, puissance=50, heureDebut="07:00:00", heureFin="10:00:00"),
        ],
        "expected": {
            "puissance_max": 195
        }
    })

    scenarios.append({
        "name": "avec_pm",
        "description": "Consommations de soiree incluant un chevauchement court.",
        "consommations": [
            Consommation(id=None, idMateriel=26, puissance=120, heureDebut="20:00:00", heureFin="22:00:00"),
            Consommation(id=None, idMateriel=27, puissance=80, heureDebut="21:00:00", heureFin="21:30:00"),
        ],
        "expected": {
            "puissance_max": 200
        }
    })

    scenarios.append({
        "name": "vide",
        "description": "Aucune consommation.",
        "consommations": [],
        "expected": {
            "puissance_max": 0
        }
    })

    return scenarios


def get_test_data_consommation_totale():
    """
    Jeux de donnees pour calculerConsommationTotale.

    energy_wh est calculee manuellement: puissance * duree(heures).
    """
    scenarios = []

    scenarios.append({
        "name": "base_jour",
        "description": "Trois charges simples dans la journee.",
        "consommations": [
            Consommation(id=None, idMateriel=31, puissance=75, heureDebut="19:00:00", heureFin="21:00:00"),
            Consommation(id=None, idMateriel=32, puissance=100, heureDebut="22:00:00", heureFin="23:00:00"),
            Consommation(id=None, idMateriel=33, puissance=200, heureDebut="00:00:00", heureFin="02:00:00"),
        ],
        "expected": {
            "consommation_totale_wh": 650.0
        }
    })

    scenarios.append({
        "name": "traverse_minuit",
        "description": "Une charge traverse minuit (22:00->06:00).",
        "consommations": [
            Consommation(id=None, idMateriel=34, puissance=70, heureDebut="22:00:00", heureFin="06:00:00"),
        ],
        "expected": {
            "consommation_totale_wh": 560.0
        }
    })

    scenarios.append({
        "name": "format_heure_standard",
        "description": "Heures au format HH:MM:SS conforme au service actuel.",
        "consommations": [
            Consommation(id=None, idMateriel=35, puissance=120, heureDebut="09:15:00", heureFin="10:45:00"),
        ],
        "expected": {
            "consommation_totale_wh": 180.0
        }
    })

    scenarios.append({
        "name": "vide",
        "description": "Aucune consommation.",
        "consommations": [],
        "expected": {
            "consommation_totale_wh": 0.0
        }
    })

    return scenarios


def print_test_data():
    """Execute les fonctions du service et valide les resultats."""

    materiel_service, consommation_service = build_services_with_materiels()

    print("=" * 72)
    print("VALIDATION MATERIELSERVICE")
    print("=" * 72)
    print(f"Materiels enregistres: {materiel_service.count()}")
    for row in materiel_service.findAll():
        print(f"  - id={row[0]}, nom={row[1]}")

    print("\n" + "=" * 72)
    print("VALIDATION calculerCapaciteBatterieRequise")
    print("=" * 72)
    for scenario in get_test_data_calculer_capacite_batterie():
        run_case_capacite(
            consommation_service,
            scenario["name"],
            scenario["consommations"],
            scenario["expected"]["capacite_totale_wh"],
        )

    print("\n" + "=" * 72)
    print("VALIDATION calculerPuissanceMaxSimultanee")
    print("=" * 72)
    for scenario in get_test_data_puissance_max_simultanee():
        run_case_puissance_max(
            consommation_service,
            scenario["name"],
            scenario["consommations"],
            scenario["expected"]["puissance_max"],
        )

    print("\n" + "=" * 72)
    print("VALIDATION calculerConsommationTotale")
    print("=" * 72)
    for scenario in get_test_data_consommation_totale():
        run_case_conso_totale(
            consommation_service,
            scenario["name"],
            scenario["consommations"],
            scenario["expected"]["consommation_totale_wh"],
        )

    print("\n" + "=" * 72)
    print("TOUS LES TESTS SONT PASS")
    print("=" * 72)


if __name__ == "__main__":
    print_test_data()
