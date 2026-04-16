from Repositories.ResultatRepository import ResultatRepository


class ResultatService:

    def __init__(self, resultatRepository: ResultatRepository):
        """
        Initialise le service avec le repository.
        
        Args:
            resultatRepository: Instance de ResultatRepository
        """
        self.resultatRepository = resultatRepository
    
    def save(self, resultat):
        """Enregistre un résultat via le repository."""
        return self.resultatRepository.save(resultat)
    
    def findAll(self):
        """Récupère tous les résultats via le repository."""
        return self.resultatRepository.findAll()
    
    def findById(self, id_resultat):
        """Récupère un résultat par ID via le repository."""
        return self.resultatRepository.findById(id_resultat)
    
    def findByConfigJournee(self, idConfigJournee):
        """Récupère les résultats par configuration de journée via le repository."""
        return self.resultatRepository.findByConfigJournee(idConfigJournee)
    
    def findByRessource(self, idRessource):
        """Récupère les résultats par ressource via le repository."""
        return self.resultatRepository.findByRessource(idRessource)
    
    def update(self, id_resultat, idConfigJournee=None, idRessource=None):
        """Modifie un résultat via le repository."""
        return self.resultatRepository.update(id_resultat, idConfigJournee, idRessource)
    
    def delete(self, id_resultat):
        """Supprime un résultat via le repository."""
        return self.resultatRepository.delete(id_resultat)
    
    def count(self):
        """Compte le nombre de résultats via le repository."""
        return self.resultatRepository.count()
