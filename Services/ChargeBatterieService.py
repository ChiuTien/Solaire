from Repositories.ChargeBatterieRepository import ChargeBatterieRepository

class ChargeBatterieService:

    def __init__(self, repo: ChargeBatterieRepository):
        self.repo = repo

    def save(self, charge):
        return self.repo.save(charge)

    def findAll(self):
        return self.repo.findAll()

    def findById(self, id_charge):
        return self.repo.findById(id_charge)

    def delete(self, id_charge):
        return self.repo.delete(id_charge)