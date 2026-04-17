class Batterie:
    """
    Modèle pour représenter une batterie.
    
    Attributs:
        id: Identifiant unique de la batterie
        capaciteTheorique: Capacité théorique en Wh (nullable - calculée par le programme)
        capaciteReelle: Capacité réelle en Wh (nullable - calculée par le programme)
        rendement: Rendement de la batterie en pourcentage (0-100)
    """
    
    def __init__(self, rendement=100.0, capaciteTheorique=None, capaciteReelle=None, id=None):
        """
        Initialise une batterie.
        
        Args:
            rendement: Rendement en pourcentage (défaut: 100.0)
            capaciteTheorique: Capacité théorique en Wh (optionnel, sera calculée)
            capaciteReelle: Capacité réelle en Wh (optionnel, sera calculée)
            id: ID de la batterie (optionnel)
        """
        self.id = id
        self.capaciteTheorique = capaciteTheorique
        self.capaciteReelle = capaciteReelle
        self.rendement = rendement
    
    @property
    def capacite_theo(self):
        """Alias pour capaciteTheorique"""
        return self.capaciteTheorique
    
    @property
    def capacite_real(self):
        """Alias pour capaciteReelle"""
        return self.capaciteReelle
    
    def __str__(self):
        theo_str = f"{self.capaciteTheorique:.2f}Wh" if self.capaciteTheorique is not None else "À calculer"
        real_str = f"{self.capaciteReelle:.2f}Wh" if self.capaciteReelle is not None else "À calculer"
        return f"Batterie(id={self.id}, theo={theo_str}, real={real_str}, rend={self.rendement:.0f}%)"
    
    def __repr__(self):
        return self.__str__()
