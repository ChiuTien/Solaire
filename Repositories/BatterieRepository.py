from sqlalchemy import text

class BatterieRepository:
    """Repository pour gérer les batteries."""
    
    def __init__(self, connexion):
        """
        Initialise le repository.
        
        Args:
            connexion: Objet connexion SQLAlchemy
        """
        self.connexion = connexion
    
    def save(self, batterie):
        """
        Enregistre une batterie.
        
        Args:
            batterie: Objet Batterie à enregistrer
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            requete = """
                INSERT INTO Batterie (capaciteTheorique, capaciteReelle, rendement)
                VALUES (:capaciteTheorique, :capaciteReelle, :rendement)
            """
            self.connexion.execute(text(requete), {
                "capaciteTheorique": batterie.capaciteTheorique,
                "capaciteReelle": batterie.capaciteReelle,
                "rendement": batterie.rendement
            })
            self.connexion.commit()
            print(f"✓ Batterie enregistrée avec succès (rendement: {batterie.rendement}%)")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de l'enregistrement de la batterie: {e}")
            return False
    
    def findAll(self):
        """
        Récupère toutes les batteries.
        
        Returns:
            list: Liste de tuples (id, capaciteTheorique, capaciteReelle, rendement) ou None
        """
        try:
            requete = "SELECT id, capaciteTheorique, capaciteReelle, rendement FROM Batterie ORDER BY id"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findById(self, id_batterie):
        """
        Récupère une batterie par son ID.
        
        Args:
            id_batterie: ID de la batterie
        
        Returns:
            tuple: (id, capaciteTheorique, capaciteReelle, rendement) ou None
        """
        try:
            requete = "SELECT id, capaciteTheorique, capaciteReelle, rendement FROM Batterie WHERE id = :id"
            resultat = self.connexion.execute(text(requete), {"id": id_batterie})
            return resultat.fetchone()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
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
        try:
            updates = []
            params = {"id": id_batterie}
            
            if capaciteTheorique is not None:
                updates.append("capaciteTheorique = :capaciteTheorique")
                params["capaciteTheorique"] = capaciteTheorique
            
            if capaciteReelle is not None:
                updates.append("capaciteReelle = :capaciteReelle")
                params["capaciteReelle"] = capaciteReelle
            
            if rendement is not None:
                updates.append("rendement = :rendement")
                params["rendement"] = rendement
            
            if not updates:
                return False
            
            requete = f"UPDATE Batterie SET {', '.join(updates)} WHERE id = :id"
            self.connexion.execute(text(requete), params)
            self.connexion.commit()
            print(f"✓ Batterie {id_batterie} mise à jour avec succès")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de la mise à jour: {e}")
            return False
    
    def delete(self, id_batterie):
        """
        Supprime une batterie.
        
        Args:
            id_batterie: ID de la batterie
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            requete = "DELETE FROM Batterie WHERE id = :id"
            self.connexion.execute(text(requete), {"id": id_batterie})
            self.connexion.commit()
            print(f"✓ Batterie {id_batterie} supprimée avec succès")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de la suppression: {e}")
            return False
