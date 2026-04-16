from sqlalchemy import text

class ConsommationRepository:
    """Repository pour gérer les consommations."""
    
    def __init__(self, connexion):
        """
        Initialise le repository.
        
        Args:
            connexion: Objet connexion SQLAlchemy
        """
        self.connexion = connexion
    
    def save(self, consommation):
        """
        Enregistre une consommation.
        
        Args:
            consommation: Objet Consommation à enregistrer
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            requete = """
                INSERT INTO Consommation (idMateriel, puissance, heureDebut, heureFin)
                VALUES (:idMateriel, :puissance, :heureDebut, :heureFin)
            """
            self.connexion.execute(text(requete), {
                "idMateriel": consommation.idMateriel,
                "puissance": consommation.puissance,
                "heureDebut": consommation.heureDebut,
                "heureFin": consommation.heureFin
            })
            self.connexion.commit()
            print(f"✓ Consommation enregistrée avec succès.")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de l'enregistrement: {e}")
            return False
    
    def findAll(self):
        """Récupère toutes les consommations."""
        try:
            requete = "SELECT id, idMateriel, puissance, heureDebut, heureFin FROM Consommation"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findById(self, id_consommation):
        """Récupère une consommation par ID."""
        try:
            requete = "SELECT id, idMateriel, puissance, heureDebut, heureFin FROM Consommation WHERE id = :id"
            resultat = self.connexion.execute(text(requete), {"id": id_consommation})
            return resultat.fetchone()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findByMateriel(self, idMateriel):
        """Récupère les consommations d'un matériel."""
        try:
            requete = "SELECT id, idMateriel, puissance, heureDebut, heureFin FROM Consommation WHERE idMateriel = :idMateriel"
            resultat = self.connexion.execute(text(requete), {"idMateriel": idMateriel})
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def update(self, id_consommation, idMateriel=None, puissance=None, heureDebut=None, heureFin=None):
        """Modifie une consommation."""
        try:
            consommation = self.findById(id_consommation)
            if not consommation:
                print(f"✗ Consommation {id_consommation} non trouvée")
                return False
            
            nouveau_idMateriel = idMateriel or consommation[1]
            nouvelle_puissance = puissance or consommation[2]
            nouveau_heureDebut = heureDebut or consommation[3]
            nouveau_heureFin = heureFin or consommation[4]
            
            requete = """
                UPDATE Consommation
                SET idMateriel = :idMateriel, puissance = :puissance, heureDebut = :heureDebut, heureFin = :heureFin
                WHERE id = :id
            """
            self.connexion.execute(text(requete), {
                "idMateriel": nouveau_idMateriel,
                "puissance": nouvelle_puissance,
                "heureDebut": nouveau_heureDebut,
                "heureFin": nouveau_heureFin,
                "id": id_consommation
            })
            self.connexion.commit()
            print(f"✓ Consommation {id_consommation} modifiée")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def delete(self, id_consommation):
        """Supprime une consommation."""
        try:
            requete = "DELETE FROM Consommation WHERE id = :id"
            self.connexion.execute(text(requete), {"id": id_consommation})
            self.connexion.commit()
            print(f"✓ Consommation {id_consommation} supprimée")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def count(self):
        """Compte le nombre de consommations."""
        try:
            requete = "SELECT COUNT(*) FROM Consommation"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchone()[0]
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return 0
