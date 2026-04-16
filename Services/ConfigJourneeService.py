from Repositories.ConfigJourneeRepository import ConfigJourneeRepository


class ConfigJourneeService:

    def __init__(self, configJourneeRepository: ConfigJourneeRepository):
        """
        Initialise le service avec le repository.
        
        Args:
            configJourneeRepository: Instance de ConfigJourneeRepository
        """
        self.configJourneeRepository = configJourneeRepository
    
    def save(self, configJournee):
        """Enregistre une configuration de journée via le repository."""
        return self.configJourneeRepository.save(configJournee)
    
    def findAll(self):
        """Récupère toutes les configurations via le repository."""
        return self.configJourneeRepository.findAll()
    
    def findById(self, id_config):
        """Récupère une configuration par ID via le repository."""
        return self.configJourneeRepository.findById(id_config)
    
    def findByStatut(self, idStatut):
        """Récupère les configurations par statut via le repository."""
        return self.configJourneeRepository.findByStatut(idStatut)
    
    def update(self, id_config, heureDebut=None, heureFin=None, rendement=None, idStatut=None):
        """Modifie une configuration via le repository."""
        return self.configJourneeRepository.update(id_config, heureDebut, heureFin, rendement, idStatut)
    
    def delete(self, id_config):
        """Supprime une configuration via le repository."""
        return self.configJourneeRepository.delete(id_config)
    
    def count(self):
        """Compte le nombre de configurations via le repository."""
        return self.configJourneeRepository.count()
