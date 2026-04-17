from Repositories.BatterieRepository import BatterieRepository
from Models.Batterie import Batterie

class BatterieService:
    """Service pour gérer les batteries."""
    
    def __init__(self, connexion):
        """
        Initialise le service.
        
        Args:
            connexion: Objet connexion SQLAlchemy
        """
        self.repository = BatterieRepository(connexion)
    
    def save(self, batterie):
        """
        Enregistre une batterie.
        
        Args:
            batterie: Objet Batterie
        
        Returns:
            bool: True si succès, False sinon
        """
        return self.repository.save(batterie)
    
    def findAll(self):
        """
        Récupère toutes les batteries.
        
        Returns:
            list: Liste de tuples
        """
        return self.repository.findAll()
    
    def findById(self, id_batterie):
        """
        Récupère une batterie par son ID.
        
        Args:
            id_batterie: ID de la batterie
        
        Returns:
            Batterie: Objet Batterie ou None
        """
        row = self.repository.findById(id_batterie)
        if not row:
            return None
        # row: (id, capaciteTheorique, capaciteReelle, rendement)
        return Batterie(
            id=row[0],
            capaciteTheorique=row[1],
            capaciteReelle=row[2],
            rendement=row[3]
        )
    
    def update(self, id_batterie, capaciteTheorique=None, capaciteReelle=None, rendement=None):
        """
        Met à jour une batterie.
        
        Args:
            id_batterie: ID de la batterie
            capaciteTheorique: Nouvelle capacité théorique (optionnel)
            capaciteReelle: Nouvelle capacité réelle (optionnel)
            rendement: Nouveau rendement (optionnel)
        
        Returns:
            bool: True si succès, False sinon
        """
        return self.repository.update(
            id_batterie,
            capaciteTheorique=capaciteTheorique,
            capaciteReelle=capaciteReelle,
            rendement=rendement
        )
    
    def delete(self, id_batterie):
        """
        Supprime une batterie.
        
        Args:
            id_batterie: ID de la batterie
        
        Returns:
            bool: True si succès, False sinon
        """
        return self.repository.delete(id_batterie)
