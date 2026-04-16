from sqlalchemy import text

class StatutRepository:
    """Repository pour gérer les statuts."""
    
    def __init__(self, connexion):
        """
        Initialise le repository.
        
        Args:
            connexion: Objet connexion SQLAlchemy
        """
        self.connexion = connexion
    
    def save(self, statut):
        """
        Enregistre un statut.
        
        Args:
            statut: Objet Statut à enregistrer
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            requete = """
                INSERT INTO Statut (nom)
                VALUES (:nom)
            """
            self.connexion.execute(text(requete), {
                "nom": statut.nom
            })
            self.connexion.commit()
            print(f"✓ Statut enregistré avec succès.")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de l'enregistrement: {e}")
            return False
    
    def findAll(self):
        """Récupère tous les statuts."""
        try:
            requete = "SELECT id, nom FROM Statut"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findById(self, id_statut):
        """Récupère un statut par ID."""
        try:
            requete = "SELECT id, nom FROM Statut WHERE id = :id"
            resultat = self.connexion.execute(text(requete), {"id": id_statut})
            return resultat.fetchone()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findByNom(self, nom):
        """Récupère un statut par nom."""
        try:
            requete = "SELECT id, nom FROM Statut WHERE nom = :nom"
            resultat = self.connexion.execute(text(requete), {"nom": nom})
            return resultat.fetchone()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def update(self, id_statut, nom=None):
        """Modifie un statut."""
        try:
            statut = self.findById(id_statut)
            if not statut:
                print(f"✗ Statut {id_statut} non trouvé")
                return False
            
            nouveau_nom = nom or statut[1]
            
            requete = """
                UPDATE Statut
                SET nom = :nom
                WHERE id = :id
            """
            self.connexion.execute(text(requete), {
                "nom": nouveau_nom,
                "id": id_statut
            })
            self.connexion.commit()
            print(f"✓ Statut {id_statut} modifié")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def delete(self, id_statut):
        """Supprime un statut."""
        try:
            requete = "DELETE FROM Statut WHERE id = :id"
            self.connexion.execute(text(requete), {"id": id_statut})
            self.connexion.commit()
            print(f"✓ Statut {id_statut} supprimé")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def count(self):
        """Compte le nombre de statuts."""
        try:
            requete = "SELECT COUNT(*) FROM Statut"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchone()[0]
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return 0
