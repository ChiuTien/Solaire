class ConfigJournee:
    def __init__(self, id, heureDebut, heureFin, rendement, idStatut):
        self._id = id
        self._heureDebut = heureDebut
        self._heureFin = heureFin
        self._rendement = rendement
        self._idStatut = idStatut

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def heureDebut(self):
        return self._heureDebut

    @heureDebut.setter
    def heureDebut(self, value):
        self._heureDebut = value

    @property
    def heureFin(self):
        return self._heureFin

    @heureFin.setter
    def heureFin(self, value):
        self._heureFin = value

    @property
    def rendement(self):
        return self._rendement

    @rendement.setter
    def rendement(self, value):
        if value < 0:
            raise ValueError("Rendement invalide")
        self._rendement = value

    @property
    def idStatut(self):
        return self._idStatut

    @idStatut.setter
    def idStatut(self, value):
        self._idStatut = value

    def __str__(self):
        return (
            f"ConfigJournee(id={self.id}, heureDebut={self.heureDebut}, "
            f"heureFin={self.heureFin}, rendement={self.rendement}, "
            f"idStatut={self.idStatut})"
        )