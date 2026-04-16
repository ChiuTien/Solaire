class Consommation:
    def __init__(self, id, idMateriel, puissance, heureDebut, heureFin):
        self._id = id
        self._idMateriel = idMateriel
        self._puissance = puissance
        self._heureDebut = heureDebut
        self._heureFin = heureFin

    # id
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    # idMateriel
    @property
    def idMateriel(self):
        return self._idMateriel

    @idMateriel.setter
    def idMateriel(self, value):
        self._idMateriel = value

    # puissance
    @property
    def puissance(self):
        return self._puissance

    @puissance.setter
    def puissance(self, value):
        self._puissance = value

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

    def __str__(self):
        return (
            f"Consommation(id={self.id}, idMateriel={self.idMateriel}, "
            f"puissance={self.puissance}, heureDebut={self.heureDebut}, "
            f"heureFin={self.heureFin})"
        )