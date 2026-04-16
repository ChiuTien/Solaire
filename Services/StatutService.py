from Repositories.StatutRepository import StatutRepository


class StatutService:

    def __init__(self, statutRepository: StatutRepository):
        """
        Initialise le service avec le repository.
        
        Args:
            statutRepository: Instance de StatutRepository
        """
        self.statutRepository = statutRepository
    
    def save(self, statut):
        """Enregistre un statut via le repository."""
        return self.statutRepository.save(statut)
    
    def findAll(self):
        """Récupère tous les statuts via le repository."""
        return self.statutRepository.findAll()
    
    def findById(self, id_statut):
        """Récupère un statut par ID via le repository."""
        return self.statutRepository.findById(id_statut)
    
    def findByNom(self, nom):
        """Récupère un statut par nom via le repository."""
        return self.statutRepository.findByNom(nom)
    
    def update(self, id_statut, nom=None):
        """Modifie un statut via le repository."""
        return self.statutRepository.update(id_statut, nom)
    
    def delete(self, id_statut):
        """Supprime un statut via le repository."""
        return self.statutRepository.delete(id_statut)
    
    def count(self):
        """Compte le nombre de statuts via le repository."""
        return self.statutRepository.count()
