class Consommation:
	def __init__(self, id, idMateriel, puissance, heureDebut, heureFin):
		self._id = id
		self._idMateriel = idMateriel
		self._puissance = puissance
		self._heureDebut = heureDebut
		self._heureFin = heureFin

	def get_id(self):
		return self._id

	def set_id(self, value):
		self._id = value

	def get_idMateriel(self):
		return self._idMateriel

	def set_idMateriel(self, value):
		self._idMateriel = value

	def get_puissance(self):
		return self._puissance

	def set_puissance(self, value):
		self._puissance = value

	def get_heureDebut(self):
		return self._heureDebut

	def set_heureDebut(self, value):
		self._heureDebut = value

	def get_heureFin(self):
		return self._heureFin

	def set_heureFin(self, value):
		self._heureFin = value

	def __str__(self):
		return (
			f"Consommation(id={self._id}, idMateriel={self._idMateriel}, "
			f"puissance={self._puissance}, heureDebut={self._heureDebut}, "
			f"heureFin={self._heureFin})"
		)
