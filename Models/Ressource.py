class Ressource:
	def __init__(self, id, nom, puissanceTheorique, puissanceReelle):
		self._id = id
		self._nom = nom
		self._puissanceTheorique = puissanceTheorique
		self._puissanceReelle = puissanceReelle

	def get_id(self):
		return self._id

	def set_id(self, value):
		self._id = value

	def get_nom(self):
		return self._nom

	def set_nom(self, value):
		self._nom = value

	def get_puissanceTheorique(self):
		return self._puissanceTheorique

	def set_puissanceTheorique(self, value):
		self._puissanceTheorique = value

	def get_puissanceReelle(self):
		return self._puissanceReelle

	def set_puissanceReelle(self, value):
		self._puissanceReelle = value

	def __str__(self):
		return (
			f"Ressource(id={self._id}, nom={self._nom}, "
			f"puissanceTheorique={self._puissanceTheorique}, "
			f"puissanceReelle={self._puissanceReelle})"
		)
