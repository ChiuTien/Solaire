class Materiel:
    def __init__(self, id, nom, prix):
        self._id = id
        self._nom = nom
        self._prix = prix

    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    def get_nom(self):
        return self._nom

    def set_nom(self, value):
        self._nom = value

    def get_prix(self):
        return self._prix

    def set_prix(self, value):
        self._prix = value

    def __str__(self):
        return f"{self._nom} (Price: {self._prix})"