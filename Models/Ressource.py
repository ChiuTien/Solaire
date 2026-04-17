class Ressource:
    def __init__(self, id, nom, puissanceTheorique, puissanceReelle, rendement=100.0):
        self._id = id
        self._nom = nom
        self._puissanceTheorique = puissanceTheorique
        self._puissanceReelle = puissanceReelle
        self._rendement = rendement

    # id
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    # nom
    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        self._nom = value

    # puissanceTheorique
    @property
    def puissanceTheorique(self):
        return self._puissanceTheorique

    @puissanceTheorique.setter
    def puissanceTheorique(self, value):
        self._puissanceTheorique = value

    # puissanceReelle
    @property
    def puissanceReelle(self):
        return self._puissanceReelle

    @puissanceReelle.setter
    def puissanceReelle(self, value):
        self._puissanceReelle = value

    # rendement
    @property
    def rendement(self):
        return self._rendement

    @rendement.setter
    def rendement(self, value):
        self._rendement = value

    def __str__(self):
        return (
            f"Ressource(id={self._id}, nom='{self._nom}', "
            f"puissanceTheorique={self._puissanceTheorique}, "
            f"puissanceReelle={self._puissanceReelle}, "
            f"rendement={self._rendement})"
        )