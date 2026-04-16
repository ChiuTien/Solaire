class Statut:
    def __init__(self, id, nom):
        self._id = id
        self._nom = nom

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        self._nom = value

    def __str__(self):
        return f"Statut(id={self._id}, nom={self._nom})"
