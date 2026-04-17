from sqlalchemy import text

class RessourceRepository:
    """Repository pour gérer les ressources."""
    
    def __init__(self, connexion):
        """
        Initialise le repository.
        
        Args:
            connexion: Objet connexion SQLAlchemy
        """
        self.connexion = connexion
    
    def save(self, ressource):
        """
        Enregistre une ressource.
        
        Args:
            ressource: Objet Ressource à enregistrer
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            requete = """
                INSERT INTO Ressource (nom, puissanceTheorique, puissanceReelle, rendement)
                VALUES (:nom, :puissanceTheorique, :puissanceReelle, :rendement)
            """
            self.connexion.execute(text(requete), {
                "nom": ressource.nom,
                "puissanceTheorique": ressource.puissanceTheorique,
                "puissanceReelle": ressource.puissanceReelle,
                "rendement": ressource.rendement
            })
            self.connexion.commit()
            print(f"✓ Ressource '{ressource.nom}' enregistrée avec succès.")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de l'enregistrement: {e}")
            return False
    
    def findAll(self):
        """Récupère toutes les ressources."""
        try:
            requete = "SELECT id, nom, puissanceTheorique, puissanceReelle, rendement FROM Ressource"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findById(self, id_ressource):
        """Récupère une ressource par ID."""
        try:
            requete = "SELECT id, nom, puissanceTheorique, puissanceReelle, rendement FROM Ressource WHERE id = :id"
            resultat = self.connexion.execute(text(requete), {"id": id_ressource})
            return resultat.fetchone()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findByNom(self, nom):
        """Récupère les ressources par nom (recherche partielle)."""
        try:
            requete = "SELECT id, nom, puissanceTheorique, puissanceReelle, rendement FROM Ressource WHERE nom LIKE :nom"
            resultat = self.connexion.execute(text(requete), {"nom": f"%{nom}%"})
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def update(self, id_ressource, nom=None, puissanceTheorique=None, puissanceReelle=None, rendement=None):
        """Modifie une ressource."""
        try:
            ressource = self.findById(id_ressource)
            if not ressource:
                print(f"✗ Ressource {id_ressource} non trouvée")
                return False
            
            nouveau_nom = nom or ressource[1]
            nouvelle_puissanceTheorique = puissanceTheorique or ressource[2]
            nouvelle_puissanceReelle = puissanceReelle or ressource[3]
            nouveau_rendement = rendement if rendement is not None else ressource[4]
            
            requete = """
                UPDATE Ressource
                SET nom = :nom, puissanceTheorique = :puissanceTheorique, puissanceReelle = :puissanceReelle, rendement = :rendement
                WHERE id = :id
            """
            self.connexion.execute(text(requete), {
                "nom": nouveau_nom,
                "puissanceTheorique": nouvelle_puissanceTheorique,
                "puissanceReelle": nouvelle_puissanceReelle,
                "rendement": nouveau_rendement,
                "id": id_ressource
            })
            self.connexion.commit()
            print(f"✓ Ressource {id_ressource} modifiée")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def delete(self, id_ressource):
        """Supprime une ressource."""
        try:
            requete = "DELETE FROM Ressource WHERE id = :id"
            self.connexion.execute(text(requete), {"id": id_ressource})
            self.connexion.commit()
            print(f"✓ Ressource {id_ressource} supprimée")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def count(self):
        """Compte le nombre de ressources."""
        try:
            requete = "SELECT COUNT(*) FROM Ressource"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchone()[0]
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return 0
