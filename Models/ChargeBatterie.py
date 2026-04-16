class ChargeBatterie:
    """Classe représentant une charge de batterie."""

    def __init__(self, heureDebut=None, heureFin=None, capacite=None, PuisanceNecessaire=None, id=None):
        self._id = id
        self._heureDebut = heureDebut
        self._heureFin = heureFin
        self._Capacite = capacite
        self._PuisanceNecessaire = PuisanceNecessaire

    # ID
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    # heureDebut
    @property
    def heureDebut(self):
        return self._heureDebut

    @heureDebut.setter
    def heureDebut(self, value):
        self._heureDebut = value

    # heureFin
    @property
    def heureFin(self):
        return self._heureFin

    @heureFin.setter
    def heureFin(self, value):
        self._heureFin = value

    # Capacite
    @property
    def capacite(self):
        return self._Capacite

    @capacite.setter
    def capacite(self, value):
        self._Capacite = value

    # PuisanceNecessaire
    @property
    def PuisanceNecessaire(self):
        return self._PuisanceNecessaire

    @PuisanceNecessaire.setter
    def PuisanceNecessaire(self, value):
        self._PuisanceNecessaire = value

    def __str__(self):
        return f"ChargeBatterie(id={self._id}, capacite={self._Capacite}, puissance={self._PuisanceNecessaire})"