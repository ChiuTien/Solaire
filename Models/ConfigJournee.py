class ConfigJournee:
	def __init__(self, id, heureDebut, heureFin, rendement, idRessource):
		self._id = id
		self._heureDebut = heureDebut
		self._heureFin = heureFin
		self._rendement = rendement
		self._idRessource = idRessource

	def get_id(self):
		return self._id

	def set_id(self, value):
		self._id = value

	def get_heureDebut(self):
		return self._heureDebut

	def set_heureDebut(self, value):
		self._heureDebut = value

	def get_heureFin(self):
		return self._heureFin

	def set_heureFin(self, value):
		self._heureFin = value

	def get_rendement(self):
		return self._rendement

	def set_rendement(self, value):
		self._rendement = value

	def get_idRessource(self):
		return self._idRessource

	def set_idRessource(self, value):
		self._idRessource = value

	def __str__(self):
		return (
			f"ConfigJournee(id={self._id}, heureDebut={self._heureDebut}, "
			f"heureFin={self._heureFin}, rendement={self._rendement}, "
			f"idRessource={self._idRessource})"
		)
