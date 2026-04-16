import unittest
from unittest.mock import create_autospec

from Repositories.ChargeBatterieRepository import ChargeBatterieRepository
from Services.ChargeBatterieService import ChargeBatterieService


class FakeCharge:
    def __init__(self, heureDebut, heureFin, capacite, puissance):
        self.heureDebut = heureDebut
        self.heureFin = heureFin
        self.capacite = capacite
        self.PuisanceNecessaire = puissance


class TestChargeBatterieService(unittest.TestCase):

    def setUp(self):
        self.repo_mock = create_autospec(ChargeBatterieRepository, instance=True)
        self.service = ChargeBatterieService(self.repo_mock)

    def test_save_delegate_to_repository(self):
        charge = FakeCharge("08:00", "10:00", 80.5, 12.5)
        self.repo_mock.save.return_value = True

        result = self.service.save(charge)

        self.repo_mock.save.assert_called_once_with(charge)
        self.assertTrue(result)

    def test_find_all_delegate_to_repository(self):
        self.repo_mock.findAll.return_value = [(1, "08:00", "10:00", 80.5, 12.5)]

        result = self.service.findAll()

        self.repo_mock.findAll.assert_called_once_with()
        self.assertEqual(result, [(1, "08:00", "10:00", 80.5, 12.5)])

    def test_find_by_id_delegate_to_repository(self):
        self.repo_mock.findById.return_value = (1, "08:00", "10:00", 80.5, 12.5)

        result = self.service.findById(1)

        self.repo_mock.findById.assert_called_once_with(1)
        self.assertEqual(result, (1, "08:00", "10:00", 80.5, 12.5))

    def test_delete_delegate_to_repository(self):
        self.repo_mock.delete.return_value = True

        result = self.service.delete(1)

        self.repo_mock.delete.assert_called_once_with(1)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
