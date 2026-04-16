from sqlalchemy import text

class ResultatRepository:
    """Repository pour gérer les résultats."""
    
    def __init__(self, connexion):
        """
        Initialise le repository.
        
        Args:
            connexion: Objet connexion SQLAlchemy
        """
        self.connexion = connexion
    
    def save(self, resultat):
        """
        Enregistre un résultat.
        
        Args:
            resultat: Objet Resultat à enregistrer
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            requete = """
                INSERT INTO Resultat (idConfigJournee, idRessource)
                VALUES (:idConfigJournee, :idRessource)
            """
            self.connexion.execute(text(requete), {
                "idConfigJournee": resultat.idConfigJournee,
                "idRessource": resultat.idRessource
            })
            self.connexion.commit()
            print(f"✓ Resultat enregistré avec succès.")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de l'enregistrement: {e}")
            return False
    
    def findAll(self):
        """Récupère tous les résultats."""
        try:
            requete = "SELECT id, idConfigJournee, idRessource FROM Resultat"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findById(self, id_resultat):
        """Récupère un résultat par ID."""
        try:
            requete = "SELECT id, idConfigJournee, idRessource FROM Resultat WHERE id = :id"
            resultat = self.connexion.execute(text(requete), {"id": id_resultat})
            return resultat.fetchone()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findByConfigJournee(self, idConfigJournee):
        """Récupère les résultats pour une configuration de journée."""
        try:
            requete = "SELECT id, idConfigJournee, idRessource FROM Resultat WHERE idConfigJournee = :idConfigJournee"
            resultat = self.connexion.execute(text(requete), {"idConfigJournee": idConfigJournee})
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findByRessource(self, idRessource):
        """Récupère les résultats pour une ressource."""
        try:
            requete = "SELECT id, idConfigJournee, idRessource FROM Resultat WHERE idRessource = :idRessource"
            resultat = self.connexion.execute(text(requete), {"idRessource": idRessource})
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def update(self, id_resultat, idConfigJournee=None, idRessource=None):
        """Modifie un résultat."""
        try:
            resultat = self.findById(id_resultat)
            if not resultat:
                print(f"✗ Resultat {id_resultat} non trouvé")
                return False
            
            nouveau_idConfigJournee = idConfigJournee or resultat[1]
            nouveau_idRessource = idRessource or resultat[2]
            
            requete = """
                UPDATE Resultat
                SET idConfigJournee = :idConfigJournee, idRessource = :idRessource
                WHERE id = :id
            """
            self.connexion.execute(text(requete), {
                "idConfigJournee": nouveau_idConfigJournee,
                "idRessource": nouveau_idRessource,
                "id": id_resultat
            })
            self.connexion.commit()
            print(f"✓ Resultat {id_resultat} modifié")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def delete(self, id_resultat):
        """Supprime un résultat."""
        try:
            requete = "DELETE FROM Resultat WHERE id = :id"
            self.connexion.execute(text(requete), {"id": id_resultat})
            self.connexion.commit()
            print(f"✓ Resultat {id_resultat} supprimé")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def count(self):
        """Compte le nombre de résultats."""
        try:
            requete = "SELECT COUNT(*) FROM Resultat"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchone()[0]
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return 0
