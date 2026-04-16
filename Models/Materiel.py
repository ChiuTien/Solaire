class Materiel:
    """Classe représentant un matériel."""
    
    def __init__(self, nom=None, id=None):
        """
        Initialise un matériel.
        
        Args:
            nom (str): Nom du matériel
            id (int): ID du matériel (auto-généré)
        """
        self._nom = nom
        self._id = id
    
    # Propriétés pour accès simple
    @property
    def nom(self):
        return self._nom
    
    @nom.setter
    def nom(self, value):
        self._nom = value
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
    
    # Anciennes méthodes pour compatibilité
    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    def get_nom(self):
        return self._nom

    def set_nom(self, value):
        self._nom = value

    def __str__(self):
        return f"Materiel(nom='{self._nom}', id={self._id})"
    
    def __repr__(self):
        return self.__str__()