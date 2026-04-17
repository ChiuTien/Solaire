class Ressource:
    def __init__(self, id, nom, puissanceTheorique, puissanceReelle, rendement=100.0, quantite=0, prix_unitaire=0.0, puissance_nominale=None):
        self._id = id
        self._nom = nom
        self._puissanceTheorique = puissanceTheorique
        self._puissanceReelle = puissanceReelle
        self._rendement = rendement
        self._quantite = quantite
        self._prix_unitaire = prix_unitaire
        self._puissance_nominale = puissance_nominale

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

    # quantite
    @property
    def quantite(self):
        return self._quantite

    @quantite.setter
    def quantite(self, value):
        self._quantite = value

    # prix_unitaire
    @property
    def prix_unitaire(self):
        return self._prix_unitaire

    @prix_unitaire.setter
    def prix_unitaire(self, value):
        self._prix_unitaire = value

    # puissance_nominale
    @property
    def puissance_nominale(self):
        return self._puissance_nominale

    @puissance_nominale.setter
    def puissance_nominale(self, value):
        self._puissance_nominale = value

    def __str__(self):
        return (
            f"Ressource(id={self._id}, nom='{self._nom}', "
            f"puissanceTheorique={self._puissanceTheorique}, "
            f"puissanceReelle={self._puissanceReelle}, "
            f"rendement={self._rendement}, "
            f"quantite={self._quantite}, "
            f"prix_unitaire={self._prix_unitaire}, "
            f"puissance_nominale={self._puissance_nominale})"
        )