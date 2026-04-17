from Repositories.RessourceRepository import RessourceRepository
import math


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
    
    def update(self, id_ressource, nom=None, puissanceTheorique=None, puissanceReelle=None, rendement=None, quantite=None, prix_unitaire=None, puissance_nominale=None):
        """Modifie une ressource via le repository."""
        return self.ressourceRepository.update(id_ressource, nom, puissanceTheorique, puissanceReelle, rendement, quantite, prix_unitaire, puissance_nominale)
    
    def delete(self, id_ressource):
        """Supprime une ressource via le repository."""
        return self.ressourceRepository.delete(id_ressource)
    
    def count(self):
        """Compte le nombre de ressources via le repository."""
        return self.ressourceRepository.count()
    
    def calculer_quantite_panneaux(self, puissance_reelle_requise, puissance_nominale_panneau):
        """
        Calcule le nombre de panneaux nécessaires.
        
        Formule: quantite = CEILING(puissance_reelle_requise / puissance_nominale_panneau)
        
        Args:
            puissance_reelle_requise: Puissance réelle requise (watts) = appareils + charge batterie
            puissance_nominale_panneau: Puissance nominale d'un panneau (watts) - ce que dit le vendeur
        
        Returns:
            int: Nombre de panneaux nécessaires
        """
        if puissance_nominale_panneau <= 0:
            return 0
        return math.ceil(puissance_reelle_requise / puissance_nominale_panneau)
