from sqlalchemy import text

class ChargeBatterieRepository:
    """Repository pour gérer ChargeBatterie."""

    def __init__(self, connexion):
        self.connexion = connexion

    def save(self, charge):
        try:
            requete = """
                INSERT INTO ChargeBatterie
                (heureDebut, heureFin, Capacite, PuisanceNecessaire)
                VALUES (:heureDebut, :heureFin, :capacite, :puissance)
            """

            self.connexion.execute(text(requete), {
                "heureDebut": charge.heureDebut,
                "heureFin": charge.heureFin,
                "capacite": charge.capacite,
                "puissance": charge.PuisanceNecessaire
            })

            self.connexion.commit()
            print("✓ ChargeBatterie enregistrée")
            return True

        except Exception as e:
            print(f"✗ Erreur save ChargeBatterie: {e}")
            return False

    def findAll(self):
        try:
            requete = "SELECT * FROM ChargeBatterie"
            result = self.connexion.execute(text(requete))
            return result.fetchall()
        except Exception as e:
            print(f"✗ Erreur findAll: {e}")
            return None

    def findById(self, id_charge):
        try:
            requete = "SELECT * FROM ChargeBatterie WHERE id = :id"
            result = self.connexion.execute(text(requete), {"id": id_charge})
            return result.fetchone()
        except Exception as e:
            print(f"✗ Erreur findById: {e}")
            return None

    def delete(self, id_charge):
        try:
            requete = "DELETE FROM ChargeBatterie WHERE id = :id"
            self.connexion.execute(text(requete), {"id": id_charge})
            self.connexion.commit()
            print("✓ ChargeBatterie supprimée")
            return True
        except Exception as e:
            print(f"✗ Erreur delete: {e}")
            return False