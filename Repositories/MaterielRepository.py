from sqlalchemy import text

class MaterielRepository:
    """Repository pour gérer les matériels."""
    
    def __init__(self, connexion):
        """
        Initialise le repository.
        
        Args:
            connexion: Objet connexion SQLAlchemy
        """
        self.connexion = connexion
    
    def saveMateriel(self, materiel):
        """
        Enregistre un matériel.
        
        Args:
            materiel: Objet Materiel à enregistrer
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            requete = """
                INSERT INTO Materiel (nom)
                VALUES (:nom)
            """
            self.connexion.execute(text(requete), {
                "nom": materiel.nom
            })
            self.connexion.commit()
            print(f"✓ Matériel '{materiel.nom}' enregistré avec succès.")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de l'enregistrement du matériel: {e}")
            return False
    
    def findAll(self):
        """Récupère tous les matériels."""
        try:
            requete = "SELECT id, nom FROM Materiel"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findById(self, id_materiel):
        """Récupère un matériel par ID."""
        try:
            requete = "SELECT id, nom FROM Materiel WHERE id = :id"
            resultat = self.connexion.execute(text(requete), {"id": id_materiel})
            return resultat.fetchone()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findByNom(self, nom):
        """Récupère les matériels par nom (recherche partielle)."""
        try:
            requete = "SELECT id, nom FROM Materiel WHERE nom LIKE :nom"
            resultat = self.connexion.execute(text(requete), {"nom": f"%{nom}%"})
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def update(self, id_materiel, nom=None):
        """Modifie un matériel."""
        try:
            materiel = self.findById(id_materiel)
            if not materiel:
                print(f"✗ Matériel {id_materiel} non trouvé")
                return False
            
            nouveau_nom = nom or materiel[1]
            
            requete = """
                UPDATE Materiel
                SET nom = :nom
                WHERE id = :id
            """
            self.connexion.execute(text(requete), {
                "nom": nouveau_nom,
                "id": id_materiel
            })
            self.connexion.commit()
            print(f"✓ Matériel {id_materiel} modifié")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def delete(self, id_materiel):
        """Supprime un matériel."""
        try:
            requete = "DELETE FROM Materiel WHERE id = :id"
            self.connexion.execute(text(requete), {"id": id_materiel})
            self.connexion.commit()
            print(f"✓ Matériel {id_materiel} supprimé")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def count(self):
        """Compte le nombre de matériels."""
        try:
            requete = "SELECT COUNT(*) FROM Materiel"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchone()[0]
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return 0

