from Repositories.MaterielRepository import MaterielRepository


class MaterielService:

    class _InMemoryMaterielRepository:
        """Fallback repository used when no database repository is provided."""

        def __init__(self):
            self._items = []
            self._next_id = 1

        def saveMateriel(self, materiel):
            if getattr(materiel, "id", None) is None:
                materiel.id = self._next_id
                self._next_id += 1
            self._items.append(materiel)
            return True

        def findAll(self):
            return list(self._items)

        def findById(self, id_materiel):
            return next((m for m in self._items if m.id == id_materiel), None)

        def findByNom(self, nom):
            if nom is None:
                return []
            terme = str(nom).lower()
            return [m for m in self._items if terme in (m.nom or "").lower()]

        def update(self, id_materiel, nom=None):
            materiel = self.findById(id_materiel)
            if materiel is None:
                return False
            if nom is not None:
                materiel.nom = nom
            return True

        def delete(self, id_materiel):
            for index, materiel in enumerate(self._items):
                if materiel.id == id_materiel:
                    self._items.pop(index)
                    return True
            return False

        def count(self):
            return len(self._items)

    def __init__(self, materielRepository: MaterielRepository = None):
        """
        MaterielService._init_(self, materielRepository)
        """
        self.materielRepository = materielRepository or self._InMemoryMaterielRepository()
    
    def saveMateriel(self, materiel):
        """Enregistre un matériel via le repository."""
        return self.materielRepository.saveMateriel(materiel)

    # API compatible with UI/materiel_interface.py
    def create(self, materiel):
        """Alias UI for saveMateriel."""
        return self.saveMateriel(materiel)
    
    def findAll(self):
        """Récupère tous les matériels via le repository."""
        return self.materielRepository.findAll()

    # API compatible with UI/materiel_interface.py
    def get_all(self):
        """Retourne une liste de dictionnaires pour l'affichage UI."""
        lignes = self.findAll() or []
        resultat = []
        for ligne in lignes:
            # Cas SQL tuple/list -> (id, nom)
            if isinstance(ligne, (tuple, list)):
                id_materiel = ligne[0] if len(ligne) > 0 else None
                nom = ligne[1] if len(ligne) > 1 else ""
                resultat.append({
                    "id": id_materiel,
                    "nom": nom,
                    "type": "",
                    "puissance": 0,
                })
                continue

            # Cas objet Materiel
            resultat.append({
                "id": getattr(ligne, "id", None),
                "nom": getattr(ligne, "nom", ""),
                "type": getattr(ligne, "type", ""),
                "puissance": getattr(ligne, "puissance", 0) or 0,
            })
        return resultat
    
    def findById(self, id_materiel):
        """Récupère un matériel par ID via le repository."""
        return self.materielRepository.findById(id_materiel)
    
    def findByNom(self, nom):
        """Récupère les matériels par nom via le repository."""
        return self.materielRepository.findByNom(nom)
    
    def update(self, id_materiel, nom=None):
        """Modifie un matériel via le repository."""
        # Supporte update(Materiel) utilisé par l'UI.
        if hasattr(id_materiel, "id"):
            materiel = id_materiel
            ok = self.materielRepository.update(materiel.id, getattr(materiel, "nom", None))

            # Si on est en fallback mémoire, conserver les attributs UI.
            if ok and isinstance(self.materielRepository, self._InMemoryMaterielRepository):
                courant = self.materielRepository.findById(materiel.id)
                if courant is not None:
                    courant.type = getattr(materiel, "type", "")
                    courant.puissance = getattr(materiel, "puissance", 0)
            return ok

        return self.materielRepository.update(id_materiel, nom)
    
    def delete(self, id_materiel):
        """Supprime un matériel via le repository."""
        return self.materielRepository.delete(id_materiel)
    
    def count(self):
        """Compte le nombre de matériels via le repository."""
        return self.materielRepository.count()

