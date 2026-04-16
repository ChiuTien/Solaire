from sqlalchemy import text

class ConfigJourneeRepository:
    """Repository pour gérer les configurations de journée."""
    
    def __init__(self, connexion):
        """
        Initialise le repository.
        
        Args:
            connexion: Objet connexion SQLAlchemy
        """
        self.connexion = connexion
    
    def save(self, configJournee):
        """
        Enregistre une configuration de journée.
        
        Args:
            configJournee: Objet ConfigJournee à enregistrer
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            requete = """
                INSERT INTO ConfigJournee (heureDebut, heureFin, rendement, idStatut)
                VALUES (:heureDebut, :heureFin, :rendement, :idStatut)
            """
            self.connexion.execute(text(requete), {
                "heureDebut": configJournee.heureDebut,
                "heureFin": configJournee.heureFin,
                "rendement": configJournee.rendement,
                "idStatut": configJournee.idStatut
            })
            self.connexion.commit()
            print(f"✓ ConfigJournee enregistrée avec succès.")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de l'enregistrement: {e}")
            return False
    
    def findAll(self):
        """Récupère toutes les configurations de journées."""
        try:
            requete = "SELECT id, heureDebut, heureFin, rendement, idStatut FROM ConfigJournee"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findById(self, id_config):
        """Récupère une configuration par ID."""
        try:
            requete = "SELECT id, heureDebut, heureFin, rendement, idStatut FROM ConfigJournee WHERE id = :id"
            resultat = self.connexion.execute(text(requete), {"id": id_config})
            return resultat.fetchone()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def findByStatut(self, idStatut):
        """Récupère les configurations par statut."""
        try:
            requete = "SELECT id, heureDebut, heureFin, rendement, idStatut FROM ConfigJournee WHERE idStatut = :idStatut"
            resultat = self.connexion.execute(text(requete), {"idStatut": idStatut})
            return resultat.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def update(self, id_config, heureDebut=None, heureFin=None, rendement=None, idStatut=None):
        """Modifie une configuration."""
        try:
            config = self.findById(id_config)
            if not config:
                print(f"✗ ConfigJournee {id_config} non trouvée")
                return False
            
            nouveau_heureDebut = heureDebut or config[1]
            nouveau_heureFin = heureFin or config[2]
            nouveau_rendement = rendement or config[3]
            nouveau_idStatut = idStatut or config[4]
            
            requete = """
                UPDATE ConfigJournee
                SET heureDebut = :heureDebut, heureFin = :heureFin, rendement = :rendement, idStatut = :idStatut
                WHERE id = :id
            """
            self.connexion.execute(text(requete), {
                "heureDebut": nouveau_heureDebut,
                "heureFin": nouveau_heureFin,
                "rendement": nouveau_rendement,
                "idStatut": nouveau_idStatut,
                "id": id_config
            })
            self.connexion.commit()
            print(f"✓ ConfigJournee {id_config} modifiée")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def delete(self, id_config):
        """Supprime une configuration."""
        try:
            requete = "DELETE FROM ConfigJournee WHERE id = :id"
            self.connexion.execute(text(requete), {"id": id_config})
            self.connexion.commit()
            print(f"✓ ConfigJournee {id_config} supprimée")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def count(self):
        """Compte le nombre de configurations."""
        try:
            requete = "SELECT COUNT(*) FROM ConfigJournee"
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchone()[0]
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return 0
