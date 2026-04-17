class Materiel:
    """Classe représentant un matériel."""
    
    def __init__(self, nom=None, id=None, type=None, puissance=0):
        """
        Initialise un matériel.
        
        Args:
            nom (str): Nom du matériel
            id (int): ID du matériel (auto-généré)
            type (str): Type du matériel
            puissance (float): Puissance du matériel en Watts
        """
        self._nom = nom
        self._id = id
        self._type = type
        self._puissance = puissance
    
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

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def puissance(self):
        return self._puissance

    @puissance.setter
    def puissance(self, value):
        self._puissance = value
    
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
        return (
            f"Materiel(nom='{self._nom}', id={self._id}, "
            f"type='{self._type}', puissance={self._puissance})"
        )
    
    def __repr__(self):
        return self.__str__()