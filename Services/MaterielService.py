from Repositories.MaterielRepository import MaterielRepository


class MaterielService:

    def __init__(self, materielRepository: MaterielRepository):
        """
        MaterielService._init_(self, materielRepository)
        """
        self.materielRepository = materielRepository
    
    def saveMateriel(self, materiel):
        """Enregistre un matériel via le repository."""
        return self.materielRepository.saveMateriel(materiel)
    
    def findAll(self):
        """Récupère tous les matériels via le repository."""
        return self.materielRepository.findAll()
    
    def findById(self, id_materiel):
        """Récupère un matériel par ID via le repository."""
        return self.materielRepository.findById(id_materiel)
    
    def findByNom(self, nom):
        """Récupère les matériels par nom via le repository."""
        return self.materielRepository.findByNom(nom)
    
    def update(self, id_materiel, nom=None):
        """Modifie un matériel via le repository."""
        return self.materielRepository.update(id_materiel, nom)
    
    def delete(self, id_materiel):
        """Supprime un matériel via le repository."""
        return self.materielRepository.delete(id_materiel)
    
    def count(self):
        """Compte le nombre de matériels via le repository."""
        return self.materielRepository.count()

