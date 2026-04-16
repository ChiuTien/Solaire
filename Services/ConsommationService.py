from Repositories.ConsommationRepository import ConsommationRepository
from datetime import datetime, time


class ConsommationService:

    def __init__(self, consommationRepository: ConsommationRepository):
        """
        Initialise le service avec le repository.
        
        Args:
            consommationRepository: Instance de ConsommationRepository
        """
        self.consommationRepository = consommationRepository
    
    def save(self, consommation):
        """Enregistre une consommation via le repository."""
        return self.consommationRepository.save(consommation)
    
    def findAll(self):
        """Récupère toutes les consommations via le repository."""
        return self.consommationRepository.findAll()
    
    def findById(self, id_consommation):
        """Récupère une consommation par ID via le repository."""
        return self.consommationRepository.findById(id_consommation)
    
    def findByMateriel(self, idMateriel):
        """Récupère les consommations par matériel via le repository."""
        return self.consommationRepository.findByMateriel(idMateriel)
    
    def update(self, id_consommation, idMateriel=None, puissance=None, heureDebut=None, heureFin=None):
        """Modifie une consommation via le repository."""
        return self.consommationRepository.update(id_consommation, idMateriel, puissance, heureDebut, heureFin)
    
    def delete(self, id_consommation):
        """Supprime une consommation via le repository."""
        return self.consommationRepository.delete(id_consommation)
    
    def count(self):
        """Compte le nombre de consommations via le repository."""
        return self.consommationRepository.count()
    
    def calculerCapaciteBatterieRequise(self, consommations):
        """
        Calcule la capacité totale de batterie (en Wh) nécessaire pour supporter
        tous les appareils avec leurs chevauchements horaires.
        
        Cette fonction divise la journée en intervalles basés sur les horaires des appareils,
        puis calcule la puissance totale à chaque intervalle (somme des appareils actifs).
        
        Exemple:
        - Consommation 1: 70W de 22:00 à 00:00
        - Consommation 2: 100W de 22:00 à 23:00
        
        Intervalles:
        - 22:00 à 23:00: 70W + 100W = 170W pendant 1h → 170 Wh
        - 23:00 à 00:00: 70W seul pendant 1h → 70 Wh
        
        Capacité batterie requise = 170 + 70 = 240 Wh
        
        Args:
            consommations: Liste d'objets Consommation
        
        Returns:
            dict: Dictionnaire contenant:
                - 'capacite_totale': Capacité requise en Watt-heures (Wh)
                - 'details': Liste des intervalles avec puissance et énergie
        """
        if not consommations or len(consommations) == 0:
            print("⚠ Aucune consommation à analyser")
            return {
                'capacite_totale': 0,
                'details': []
            }
        
        try:
            # Créer une liste de tous les événements (début et fin de chaque consommation)
            evenements = []
            
            for idx, consommation in enumerate(consommations):
                puissance = consommation.puissance
                heure_debut = consommation.heureDebut
                heure_fin = consommation.heureFin
                
                # Convertir les heures en objets time si elles sont des chaînes
                if isinstance(heure_debut, str):
                    heure_debut = datetime.strptime(heure_debut, "%H:%M:%S").time()
                if isinstance(heure_fin, str):
                    heure_fin = datetime.strptime(heure_fin, "%H:%M:%S").time()
                
                # Déterminer si on traverse minuit
                traverse_minuit = heure_fin < heure_debut
                
                # Créer un timestamp pour le tri
                def temps_en_secondes(t):
                    return t.hour * 3600 + t.minute * 60 + t.second
                
                temps_debut_sort = temps_en_secondes(heure_debut)
                temps_fin_sort = temps_en_secondes(heure_fin)
                
                if traverse_minuit:
                    temps_fin_sort += 24 * 3600  # Ajouter 24h pour trier après minuit
                
                # Ajouter les événements avec clé de tri
                evenements.append({
                    'temps': heure_debut,
                    'temps_sort': temps_debut_sort,
                    'type': 'debut',
                    'puissance': puissance,
                    'id': idx
                })
                evenements.append({
                    'temps': heure_fin,
                    'temps_sort': temps_fin_sort,
                    'type': 'fin',
                    'puissance': puissance,
                    'id': idx,
                    'traverse_minuit': traverse_minuit
                })
            
            # Trier les événements par la clé de tri
            evenements.sort(key=lambda x: x['temps_sort'])
            
            # Parcourir les événements et diviser en intervalles
            puissance_active = 0
            capacite_totale = 0.0
            details = []
            
            for i, evenement in enumerate(evenements):
                # Mettre à jour la puissance active
                if evenement['type'] == 'debut':
                    puissance_active += evenement['puissance']
                else:
                    puissance_active -= evenement['puissance']
                
                # Calculer l'intervalle jusqu'au prochain événement
                if i < len(evenements) - 1:
                    heure_debut = evenement['temps']
                    heure_fin = evenements[i + 1]['temps']
                    
                    # Calculer le temps écoulé
                    secs_debut = heure_debut.hour * 3600 + heure_debut.minute * 60 + heure_debut.second
                    secs_fin = heure_fin.hour * 3600 + heure_fin.minute * 60 + heure_fin.second
                    
                    # Si fin < début en secondes brutes, ça veut dire qu'on traverse minuit
                    if secs_fin < secs_debut:
                        temps_secondes = (24 * 3600 - secs_debut) + secs_fin
                    else:
                        temps_secondes = secs_fin - secs_debut
                    
                    temps_heures = temps_secondes / 3600
                    
                    # Calculer l'énergie pour cet intervalle
                    energie_wh = puissance_active * temps_heures
                    capacite_totale += energie_wh
                    
                    detail = {
                        'debut': heure_debut.strftime("%H:%M:%S"),
                        'fin': heure_fin.strftime("%H:%M:%S"),
                        'puissance': puissance_active,
                        'temps_heures': temps_heures,
                        'energie_wh': energie_wh
                    }
                    details.append(detail)
            
            # Afficher les résultats
            print("\n📊 Analyse détaillée des intervalles:\n")
            print(f"{'Début':^10} | {'Fin':^10} | {'Puissance':^12} | {'Durée':^10} | {'Énergie':^12}")
            print("─" * 70)
            
            for detail in details:
                debut = detail['debut']
                fin = detail['fin']
                puissance = detail['puissance']
                temps = detail['temps_heures']
                energie = detail['energie_wh']
                
                print(f"{debut:^10} → {fin:^10} | {puissance:>10}W | {temps:>8.2f}h | {energie:>10.2f} Wh")
            
            print("─" * 70)
            print(f"\n🔋 Capacité de batterie requise: {capacite_totale:.2f} Wh ({capacite_totale/1000:.3f} kWh)")
            
            return {
                'capacite_totale': capacite_totale,
                'details': details
            }
            
        except AttributeError as e:
            print(f"✗ Erreur d'accès aux attributs de consommation: {e}")
            return {
                'capacite_totale': 0,
                'details': []
            }
        except Exception as e:
            print(f"✗ Erreur lors du calcul: {e}")
            import traceback
            traceback.print_exc()
            return {
                'capacite_totale': 0,
                'details': []
            }
    
    def calculerPuissanceMaxSimultanee(self, consommations):
        """
        Calcule la puissance maximale instantanée (peak power) nécessaire pour supporter
        tous les appareils qui pourraient fonctionner simultanément.
        
        Cette fonction divise la journée en intervalles de temps basés sur les horaires
        des consommations, puis détermine la puissance nécessaire à chaque moment.
        
        Exemple:
        - Consommation 1: 70W de 22:00 à 24:00
        - Consommation 2: 100W de 22:00 à 23:00
        
        Intervalles:
        - 22:00 à 23:00: 70W + 100W = 170W (simultanément)
        - 23:00 à 24:00: 70W (seul)
        
        Puissance max = 170W (capacité minimale requise pour la batterie)
        
        Args:
            consommations: Liste d'objets Consommation
        
        Returns:
            dict: Dictionnaire contenant:
                - 'puissance_max': Puissance maximale en Watts
                - 'intervalle_max': Intervalle de temps où la puissance max est requise
                - 'details': Liste des détails pour chaque intervalle
        """
        if not consommations or len(consommations) == 0:
            print("⚠ Aucune consommation à analyser")
            return {
                'puissance_max': 0,
                'intervalle_max': None,
                'details': []
            }
        
        try:
            # Créer une liste de tous les événements (début et fin de chaque consommation)
            evenements = []
            
            for consommation in consommations:
                puissance = consommation.puissance
                heure_debut = consommation.heureDebut
                heure_fin = consommation.heureFin
                
                # Convertir les heures en objets time si elles sont des chaînes
                if isinstance(heure_debut, str):
                    heure_debut = datetime.strptime(heure_debut, "%H:%M:%S").time()
                if isinstance(heure_fin, str):
                    heure_fin = datetime.strptime(heure_fin, "%H:%M:%S").time()
                
                # Ajouter les événements
                evenements.append({
                    'temps': heure_debut,
                    'type': 'debut',
                    'puissance': puissance
                })
                evenements.append({
                    'temps': heure_fin,
                    'type': 'fin',
                    'puissance': puissance
                })
            
            # Trier les événements par heure
            evenements.sort(key=lambda x: x['temps'])
            
            # Parcourir les événements et calculer la puissance à chaque intervalle
            puissance_actuelle = 0
            puissance_max = 0
            intervalle_max = None
            details = []
            
            for i, evenement in enumerate(evenements):
                if evenement['type'] == 'debut':
                    puissance_actuelle += evenement['puissance']
                else:  # fin
                    puissance_actuelle -= evenement['puissance']
                
                # Enregistrer l'intervalle jusqu'au prochain événement
                if i < len(evenements) - 1:
                    heure_debut = evenement['temps']
                    heure_fin = evenements[i + 1]['temps']
                    
                    detail = {
                        'debut': heure_debut.strftime("%H:%M:%S"),
                        'fin': heure_fin.strftime("%H:%M:%S"),
                        'puissance': puissance_actuelle
                    }
                    details.append(detail)
                    
                    # Mettre à jour la puissance max
                    if puissance_actuelle > puissance_max:
                        puissance_max = puissance_actuelle
                        intervalle_max = detail
            
            # Afficher les résultats
            print("\n🔍 Analyse des intervalles de temps:\n")
            for detail in details:
                puissance_display = detail['puissance']
                debut = detail['debut']
                fin = detail['fin']
                
                if puissance_display == puissance_max:
                    print(f"⭐ {debut} → {fin}: {puissance_display}W (MAXIMUM)")
                else:
                    print(f"   {debut} → {fin}: {puissance_display}W")
            
            print(f"\n⚡ Puissance maximale instantanée requise: {puissance_max}W")
            print(f"📍 Intervalle critique: {intervalle_max['debut']} → {intervalle_max['fin']}")
            
            return {
                'puissance_max': puissance_max,
                'intervalle_max': intervalle_max,
                'details': details
            }
            
        except AttributeError as e:
            print(f"✗ Erreur d'accès aux attributs de consommation: {e}")
            return {
                'puissance_max': 0,
                'intervalle_max': None,
                'details': []
            }
        except Exception as e:
            print(f"✗ Erreur lors du calcul: {e}")
            return {
                'puissance_max': 0,
                'intervalle_max': None,
                'details': []
            }
    
    def calculerConsommationTotale(self, consommations):
        """
        Calcule la consommation totale d'énergie pour une liste de consommations.
        
        La consommation est calculée de la manière suivante:
        Énergie (Wh) = Puissance (W) × Temps (heures)
        
        Exemple:
        - Consommation 1: 75W de 19:00 à 21:00 = 75W × 2h = 150 Wh
        - Consommation 2: 100W de 22:00 à 23:00 = 100W × 1h = 100 Wh
        - Consommation totale = 150 + 100 = 250 Wh
        
        Args:
            consommations: Liste d'objets Consommation
        
        Returns:
            float: Consommation totale en Watt-heures (Wh)
        """
        if not consommations or len(consommations) == 0:
            print("⚠ Aucune consommation à calculer")
            return 0.0
        
        consommation_totale = 0.0
        
        for consommation in consommations:
            try:
                # Récupérer la puissance (en Watts)
                puissance = consommation.puissance
                
                # Récupérer les heures de début et fin
                heure_debut = consommation.heureDebut
                heure_fin = consommation.heureFin
                
                # Convertir les heures en objets time si elles sont des chaînes
                if isinstance(heure_debut, str):
                    heure_debut = datetime.strptime(heure_debut, "%H:%M:%S").time()
                if isinstance(heure_fin, str):
                    heure_fin = datetime.strptime(heure_fin, "%H:%M:%S").time()
                
                # Calculer le temps écoulé en heures
                debut = datetime.combine(datetime.today(), heure_debut)
                fin = datetime.combine(datetime.today(), heure_fin)
                
                # Gérer le cas où la fin est le jour suivant (par exemple 22:00 à 06:00)
                if fin < debut:
                    fin = fin.replace(day=fin.day + 1)
                
                temps_heures = (fin - debut).total_seconds() / 3600
                
                # Calculer la consommation pour cette ligne (Wh)
                consommation_wh = puissance * temps_heures
                
                # Ajouter à la consommation totale
                consommation_totale += consommation_wh
                
                print(f"✓ {puissance}W × {temps_heures:.2f}h = {consommation_wh:.2f} Wh")
                
            except AttributeError as e:
                print(f"✗ Erreur d'accès aux attributs de consommation: {e}")
                continue
            except Exception as e:
                print(f"✗ Erreur lors du calcul de consommation: {e}")
                continue
        
        print(f"\n📊 Consommation totale: {consommation_totale:.2f} Wh ({consommation_totale/1000:.3f} kWh)")
        return consommation_totale
