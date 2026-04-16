from Repositories.ChargeBatterieRepository import ChargeBatterieRepository
from datetime import datetime


class ChargeBatterieService:

    def __init__(self, repo: ChargeBatterieRepository):
        """
        Initialise le service avec le repository.
        
        Args:
            repo: Instance de ChargeBatterieRepository
        """
        self.repo = repo

    def save(self, charge):
        """Enregistre une charge de batterie via le repository."""
        return self.repo.save(charge)

    def findAll(self):
        """Récupère toutes les charges de batterie via le repository."""
        return self.repo.findAll()

    def findById(self, id_charge):
        """Récupère une charge de batterie par ID via le repository."""
        return self.repo.findById(id_charge)

    def update(self, id_charge, heureDebut=None, heureFin=None, capacite=None, puissanceNecessaire=None):
        """Modifie une charge de batterie via le repository."""
        return self.repo.update(id_charge, heureDebut, heureFin, capacite, puissanceNecessaire)

    def delete(self, id_charge):
        """Supprime une charge de batterie via le repository."""
        return self.repo.delete(id_charge)

    def count(self):
        """Compte le nombre de charges de batterie via le repository."""
        return self.repo.count()
    
    def calculerPuissanceNecessaire(self, heureDebut, heureFin, capaciteBatterie):
        """
        Calcule la puissance nécessaire que doit fournir un panneau solaire
        pour charger la batterie dans le laps de temps donné.
        
        Formule:
        Puissance (W) = Capacité (Wh) / Temps (heures)
        
        Exemple:
        - Capacité batterie: 240Wh
        - Charge de 10:00 à 14:00 (4 heures)
        - Puissance requise = 240Wh / 4h = 60W
        
        Args:
            heureDebut: Heure de début de charge (str "HH:MM:SS" ou time)
            heureFin: Heure de fin de charge (str "HH:MM:SS" ou time)
            capaciteBatterie: Capacité de la batterie en Wh (float)
        
        Returns:
            dict: Dictionnaire contenant:
                - 'puissance_necessaire': Puissance requise en Watts (W)
                - 'temps_heures': Temps de charge en heures
                - 'details': Détails du calcul
        """
        if not heureDebut or not heureFin or capaciteBatterie <= 0:
            print("⚠ Paramètres invalides")
            return {
                'puissance_necessaire': 0,
                'temps_heures': 0,
                'details': None
            }
        
        try:
            # Convertir les heures en objets time si elles sont des chaînes
            if isinstance(heureDebut, str):
                heureDebut = datetime.strptime(heureDebut, "%H:%M:%S").time()
            if isinstance(heureFin, str):
                heureFin = datetime.strptime(heureFin, "%H:%M:%S").time()
            
            # Calculer le temps de charge en secondes
            secs_debut = heureDebut.hour * 3600 + heureDebut.minute * 60 + heureDebut.second
            secs_fin = heureFin.hour * 3600 + heureFin.minute * 60 + heureFin.second
            
            # Vérifier si on traverse minuit
            if secs_fin < secs_debut:
                temps_secondes = (24 * 3600 - secs_debut) + secs_fin
            else:
                temps_secondes = secs_fin - secs_debut
            
            # Éviter division par zéro
            if temps_secondes == 0:
                print("⚠ La durée de charge doit être > 0")
                return {
                    'puissance_necessaire': 0,
                    'temps_heures': 0,
                    'details': None
                }
            
            temps_heures = temps_secondes / 3600
            
            # Calculer la puissance nécessaire
            puissance_necessaire = capaciteBatterie / temps_heures
            
            # Préparer les détails
            details = {
                'heureDebut': heureDebut.strftime("%H:%M:%S"),
                'heureFin': heureFin.strftime("%H:%M:%S"),
                'capaciteBatterie': capaciteBatterie,
                'temps_heures': temps_heures
            }
            
            # Afficher les résultats
            print("\n☀️ Calcul de la puissance du panneau solaire\n")
            print(f"  Heure de début  : {details['heureDebut']}")
            print(f"  Heure de fin    : {details['heureFin']}")
            print(f"  Temps de charge : {temps_heures:.2f} h")
            print(f"  Capacité batterie: {capaciteBatterie:.2f} Wh")
            print("  " + "─" * 52)
            print(f"  Formule: Puissance = Capacité / Temps")
            print(f"  Puissance = {capaciteBatterie:.2f}Wh / {temps_heures:.2f}h")
            print(f"\n  ⚡ Puissance nécessaire: {puissance_necessaire:.2f}W")
            
            return {
                'puissance_necessaire': puissance_necessaire,
                'temps_heures': temps_heures,
                'details': details
            }
            
        except ValueError as e:
            print(f"✗ Erreur de conversion d'heure: {e}")
            return {
                'puissance_necessaire': 0,
                'temps_heures': 0,
                'details': None
            }
        except Exception as e:
            print(f"✗ Erreur lors du calcul: {e}")
            import traceback
            traceback.print_exc()
            return {
                'puissance_necessaire': 0,
                'temps_heures': 0,
                'details': None
            }