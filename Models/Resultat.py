class Resultat:
	def __init__(self, id, idConfigJournee, idRessource):
		self._id = id
		self._idConfigJournee = idConfigJournee
		self._idRessource = idRessource

	def get_id(self):
		return self._id

	def set_id(self, value):
		self._id = value

	def get_idConfigJournee(self):
		return self._idConfigJournee

	def set_idConfigJournee(self, value):
		self._idConfigJournee = value

	def get_idRessource(self):
		return self._idRessource

	def set_idRessource(self, value):
		self._idRessource = value

	def __str__(self):
		return (
			f"Resultat(id={self._id}, idConfigJournee={self._idConfigJournee}, "
			f"idRessource={self._idRessource})"
		)
