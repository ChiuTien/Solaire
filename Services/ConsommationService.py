from Repositories.ConsommationRepository import ConsommationRepository


class ConsommationService:

    def __init__(self, consommationRepository: ConsommationRepository):
        """
        Initialise le service avec le repository.
        
        Args:
            consommationRepository: Instance de ConsommationRepository
        """
        self.consommationRepository = consommationRepository
    
    def save(self, consommation):
        """Enregistre une consommation via le repository."""
        return self.consommationRepository.save(consommation)
    
    def findAll(self):
        """Récupère toutes les consommations via le repository."""
        return self.consommationRepository.findAll()
    
    def findById(self, id_consommation):
        """Récupère une consommation par ID via le repository."""
        return self.consommationRepository.findById(id_consommation)
    
    def findByMateriel(self, idMateriel):
        """Récupère les consommations par matériel via le repository."""
        return self.consommationRepository.findByMateriel(idMateriel)
    
    def update(self, id_consommation, idMateriel=None, puissance=None, heureDebut=None, heureFin=None):
        """Modifie une consommation via le repository."""
        return self.consommationRepository.update(id_consommation, idMateriel, puissance, heureDebut, heureFin)
    
    def delete(self, id_consommation):
        """Supprime une consommation via le repository."""
        return self.consommationRepository.delete(id_consommation)
    
    def count(self):
        """Compte le nombre de consommations via le repository."""
        return self.consommationRepository.count()
