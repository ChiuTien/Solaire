class MaterielRepository:
def saveMateriel(self, materiel):
    try:
        cursos = self.connexion.cursor()
        requete = """
            INSERT INTO Materiel (nom) VALUES (%s)
        """
        cursos.execute(requete, (materiel.nom,))
        self.connexion.commit()
        print("Materiel enregistré avec succès.")
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du materiel: {e}")
        return False

