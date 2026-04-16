from Repositories.RessourceRepository import RessourceRepository


class RessourceService:

    def __init__(self, ressourceRepository: RessourceRepository):
        """
        Initialise le service avec le repository.
        
        Args:
            ressourceRepository: Instance de RessourceRepository
        """
        self.ressourceRepository = ressourceRepository
    
    def save(self, ressource):
        """Enregistre une ressource via le repository."""
        return self.ressourceRepository.save(ressource)
    
    def findAll(self):
        """Récupère toutes les ressources via le repository."""
        return self.ressourceRepository.findAll()
    
    def findById(self, id_ressource):
        """Récupère une ressource par ID via le repository."""
        return self.ressourceRepository.findById(id_ressource)
    
    def findByNom(self, nom):
        """Récupère les ressources par nom via le repository."""
        return self.ressourceRepository.findByNom(nom)
    
    def update(self, id_ressource, nom=None, puissanceTheorique=None, puissanceReelle=None):
        """Modifie une ressource via le repository."""
        return self.ressourceRepository.update(id_ressource, nom, puissanceTheorique, puissanceReelle)
    
    def delete(self, id_ressource):
        """Supprime une ressource via le repository."""
        return self.ressourceRepository.delete(id_ressource)
    
    def count(self):
        """Compte le nombre de ressources via le repository."""
        return self.ressourceRepository.count()
