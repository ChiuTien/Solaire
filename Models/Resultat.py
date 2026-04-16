class Resultat:
    def __init__(self, id, idConfigJournee, idRessource):
        self._id = id
        self._idConfigJournee = idConfigJournee
        self._idRessource = idRessource

    # id
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    # idConfigJournee
    @property
    def idConfigJournee(self):
        return self._idConfigJournee

    @idConfigJournee.setter
    def idConfigJournee(self, value):
        self._idConfigJournee = value

    # idRessource
    @property
    def idRessource(self):
        return self._idRessource

    @idRessource.setter
    def idRessource(self, value):
        self._idRessource = value

    def __str__(self):
        return (
            f"Resultat(id={self._id}, idConfigJournee={self._idConfigJournee}, "
            f"idRessource={self._idRessource})"
        )