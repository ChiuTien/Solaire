from Repositories.ConsommationRepository import ConsommationRepository
from datetime import datetime, time


class ConsommationService:

    def __init__(self, consommationRepository: ConsommationRepository = None):
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
    
    def calculerPuissancePanneauRequise(self, consommations, heureDebut, heureFin):
        """
        Calcule la puissance maximale que doit fournir un panneau solaire
        pendant un intervalle de temps donné, en tenant compte des chevauchements
        de consommations.
        
        Cette fonction analyse toutes les consommations qui se produisent (au moins
        partiellement) pendant l'intervalle [heureDebut, heureFin] et retourne
        la puissance maximale instantanée requise.
        
        Exemple:
        - Intervalle de charge: 10:00 à 14:00
        - Consommations:
          * 09:00-11:00: 75W (chevauchement 10:00-11:00)
          * 10:30-13:00: 100W (chevauchement 10:30-13:00)
          * 13:00-15:00: 50W (chevauchement 13:00-14:00)
        
        Puissances par sous-intervalle:
        - 10:00-10:30: 75W
        - 10:30-11:00: 175W ⚡ MAX
        - 11:00-13:00: 100W
        - 13:00-14:00: 150W
        
        Puissance panneau requise = 175W
        
        Args:
            consommations: Liste d'objets Consommation
            heureDebut: Heure de début de l'intervalle (str "HH:MM:SS" ou time)
            heureFin: Heure de fin de l'intervalle (str "HH:MM:SS" ou time)
        
        Returns:
            dict: Dictionnaire contenant:
                - 'puissance_max': Puissance maximale requise en Watts
                - 'intervalle_max': Sous-intervalle où le max est atteint
                - 'details': Liste des détails pour chaque sous-intervalle
        """
        if not consommations or len(consommations) == 0:
            print("⚠ Aucune consommation à analyser")
            return {
                'puissance_max': 0,
                'intervalle_max': None,
                'details': []
            }
        
        try:
            # Convertir les heures de l'intervalle en objets time
            if isinstance(heureDebut, str):
                heureDebut = datetime.strptime(heureDebut, "%H:%M:%S").time()
            if isinstance(heureFin, str):
                heureFin = datetime.strptime(heureFin, "%H:%M:%S").time()
            
            # Créer une liste d'événements pour les consommations
            evenements = []
            
            for idx, consommation in enumerate(consommations):
                puissance = consommation.puissance
                conso_debut = consommation.heureDebut
                conso_fin = consommation.heureFin
                
                # Convertir en objets time si nécessaire
                if isinstance(conso_debut, str):
                    conso_debut = datetime.strptime(conso_debut, "%H:%M:%S").time()
                if isinstance(conso_fin, str):
                    conso_fin = datetime.strptime(conso_fin, "%H:%M:%S").time()
                
                # Vérifier si la consommation chevauchie l'intervalle
                # Convertir en secondes pour comparaison
                def temps_en_secs(t):
                    return t.hour * 3600 + t.minute * 60 + t.second
                
                conso_debut_secs = temps_en_secs(conso_debut)
                conso_fin_secs = temps_en_secs(conso_fin)
                intervalle_debut_secs = temps_en_secs(heureDebut)
                intervalle_fin_secs = temps_en_secs(heureFin)
                
                # Gérer les traversées de minuit
                traverse_minuit = conso_fin_secs < conso_debut_secs
                
                # Vérifier le chevauchement
                if traverse_minuit:
                    conso_fin_secs += 24 * 3600
                
                if intervalle_fin_secs < intervalle_debut_secs:
                    intervalle_fin_secs += 24 * 3600
                
                # Vérifier si il y a chevauchement
                if conso_fin_secs > intervalle_debut_secs and conso_debut_secs < intervalle_fin_secs:
                    # Ajouter les événements
                    evenements.append({
                        'temps': max(conso_debut_secs, intervalle_debut_secs),
                        'type': 'debut',
                        'puissance': puissance
                    })
                    evenements.append({
                        'temps': min(conso_fin_secs, intervalle_fin_secs),
                        'type': 'fin',
                        'puissance': puissance
                    })
            
            # Ajouter les événements "limites" de l'intervalle
            evenements.append({
                'temps': temps_en_secs(heureDebut),
                'type': 'limite_debut',
            })
            evenements.append({
                'temps': temps_en_secs(heureFin),
                'type': 'limite_fin',
            })
            
            # Trier les événements
            evenements.sort(key=lambda x: x['temps'])
            
            # Parcourir et calculer les puissances par intervalle
            puissance_active = 0
            puissance_max = 0
            intervalle_max = None
            details = []
            
            for i, evenement in enumerate(evenements):
                if evenement['type'] == 'debut':
                    puissance_active += evenement['puissance']
                elif evenement['type'] == 'fin':
                    puissance_active -= evenement['puissance']
                
                # Créer un intervalle jusqu'au prochain événement
                if i < len(evenements) - 1 and evenement['type'] != 'limite_fin':
                    temps_debut = evenement['temps']
                    temps_fin = evenements[i + 1]['temps']
                    
                    if temps_fin > temps_debut:
                        # Convertir en heure:minute:seconde
                        heure_debut_str = f"{(temps_debut // 3600) % 24:02d}:{(temps_debut % 3600) // 60:02d}:{temps_debut % 60:02d}"
                        heure_fin_str = f"{(temps_fin // 3600) % 24:02d}:{(temps_fin % 3600) // 60:02d}:{temps_fin % 60:02d}"
                        
                        detail = {
                            'debut': heure_debut_str,
                            'fin': heure_fin_str,
                            'puissance': puissance_active
                        }
                        details.append(detail)
                        
                        # Mettre à jour la puissance max
                        if puissance_active > puissance_max:
                            puissance_max = puissance_active
                            intervalle_max = detail
            
            # Afficher les résultats
            print("\n☀️ Analyse de la puissance du panneau solaire:\n")
            print(f"{'Début':^10} | {'Fin':^10} | {'Puissance':^12}")
            print("─" * 50)
            
            for detail in details:
                debut = detail['debut']
                fin = detail['fin']
                puissance = detail['puissance']
                
                if puissance == puissance_max and puissance_max > 0:
                    print(f"{debut:^10} → {fin:^10} | {puissance:>10}W ⚡")
                else:
                    print(f"{debut:^10} → {fin:^10} | {puissance:>10}W")
            
            print("─" * 50)
            print(f"\n⚡ Puissance maximale du panneau requise: {puissance_max:.2f}W")
            if intervalle_max:
                print(f"📍 Intervalle critique: {intervalle_max['debut']} → {intervalle_max['fin']}")
            
            return {
                'puissance_max': puissance_max,
                'intervalle_max': intervalle_max,
                'details': details
            }
            
        except AttributeError as e:
            print(f"✗ Erreur d'accès aux attributs: {e}")
            return {
                'puissance_max': 0,
                'intervalle_max': None,
                'details': []
            }
        except Exception as e:
            print(f"✗ Erreur lors du calcul: {e}")
            import traceback
            traceback.print_exc()
            return {
                'puissance_max': 0,
                'intervalle_max': None,
                'details': []
            }
    
    def calculerPuissanceTotalePanneau(self, consommations, heureDebut, heureFin, puissanceChargeBatterie, rendement=100):
        """
        Calcule la puissance TOTALE que doit fournir le panneau solaire pour:
        1. Alimenter les appareils
        2. Charger la batterie en même temps
        
        Tenant compte du rendement du panneau (intensité du soleil).
        
        Formule:
        Puissance requise (utilisable) = max(puissance appareils) + puissance charge batterie
        Puissance théorique panneau = Puissance requise / (rendement / 100)
        
        Exemple:
        - Consommations appareils max: 175W (dans l'intervalle)
        - Puissance pour charger batterie: 60W
        - Puissance requise: 175W + 60W = 235W
        - Rendement: 80%
        - Puissance théorique panneau: 235W / 0.80 = 293.75W
        
        Args:
            consommations: Liste d'objets Consommation
            heureDebut: Heure de début de l'intervalle (str "HH:MM:SS" ou time)
            heureFin: Heure de fin de l'intervalle (str "HH:MM:SS" ou time)
            puissanceChargeBatterie: Puissance pour charger la batterie en W (float)
            rendement: Rendement du panneau en % (0-100). Défaut: 100% (rendement parfait)
        
        Returns:
            dict: Dictionnaire contenant:
                - 'puissance_requise': Puissance totale requise (utilisable)
                - 'puissance_theorique': Puissance théorique du panneau (avec rendement appliqué)
                - 'puissance_appareils': Puissance max des appareils
                - 'puissance_batterie': Puissance de charge batterie
                - 'rendement': Rendement appliqué
                - 'details': Détails des calculs
        """
        if not consommations or len(consommations) == 0:
            print("⚠ Aucune consommation à analyser")
            puissance_theorique = puissanceChargeBatterie / (rendement / 100) if rendement > 0 else puissanceChargeBatterie
            return {
                'puissance_requise': puissanceChargeBatterie,
                'puissance_theorique': puissance_theorique,
                'puissance_appareils': 0,
                'puissance_batterie': puissanceChargeBatterie,
                'rendement': rendement,
                'details': None
            }
        
        try:
            # Récupérer la puissance max des appareils dans cet intervalle
            resultat_appareils = self.calculerPuissancePanneauRequise(consommations, heureDebut, heureFin)
            puissance_appareils_max = resultat_appareils['puissance_max']
            
            # Calculer la puissance requise (utilisable)
            puissance_requise = puissance_appareils_max + puissanceChargeBatterie
            
            # Calculer la puissance théorique du panneau avec le rendement
            if rendement > 0:
                puissance_theorique = puissance_requise / (rendement / 100)
            else:
                puissance_theorique = float('inf')  # Rendement 0% = impossible
            
            # Afficher les résultats
            print("\n🔌 Calcul de la puissance TOTALE du panneau solaire\n")
            print(f"  Intervalle: {heureDebut} → {heureFin}")
            print(f"  Rendement du panneau      : {rendement:.1f}%")
            print(f"  Puissance max appareils    : {puissance_appareils_max:.2f}W")
            print(f"  Puissance charge batterie  : {puissanceChargeBatterie:.2f}W")
            print("  " + "─" * 58)
            print(f"  Formule: Puissance requise = Appareils + Batterie")
            print(f"  Puissance requise = {puissance_appareils_max:.2f}W + {puissanceChargeBatterie:.2f}W = {puissance_requise:.2f}W")
            print()
            print(f"  Formule: Puissance théorique = Puissance requise / (Rendement / 100)")
            print(f"  Puissance théorique = {puissance_requise:.2f}W / {rendement/100:.2f} = {puissance_theorique:.2f}W")
            print(f"\n  ⚡ Puissance requise (utilisable): {puissance_requise:.2f}W")
            print(f"  ☀️  Puissance théorique panneau:  {puissance_theorique:.2f}W")
            
            details = {
                'intervalle_debut': heureDebut,
                'intervalle_fin': heureFin,
                'puissance_appareils': puissance_appareils_max,
                'puissance_batterie': puissanceChargeBatterie,
                'puissance_requise': puissance_requise,
                'rendement': rendement,
                'puissance_theorique': puissance_theorique,
                'intervalle_critique_appareils': resultat_appareils['intervalle_max']
            }
            
            return {
                'puissance_requise': puissance_requise,
                'puissance_theorique': puissance_theorique,
                'puissance_appareils': puissance_appareils_max,
                'puissance_batterie': puissanceChargeBatterie,
                'rendement': rendement,
                'details': details
            }
            
        except Exception as e:
            print(f"✗ Erreur lors du calcul: {e}")
            import traceback
            traceback.print_exc()
            return {
                'puissance_requise': 0,
                'puissance_theorique': 0,
                'puissance_appareils': 0,
                'puissance_batterie': puissanceChargeBatterie,
                'rendement': rendement,
                'details': None
            }
    
    def calculerBesoinsParPeriode(self, consommations, configJournee_matin, configJournee_apres, 
                                   heureChargeDebut, heureChargeFin, capaciteBatterie):
        """
        Calcule les besoins pratiques (puissance utilisable) pour chaque période de la journée.
        
        Matin: Appareils (période entière) + Batterie en charge (fenêtre spécifique)
        Après-midi: Appareils (période entière)
        Soir: Batterie seule (décharge)
        
        ⚠️ IMPORTANT: On analyse les périodes ENTIÈRES pour trouver les appareils,
        mais la batterie ne charge que durant heureChargeDebut → heureChargeFin.
        
        Args:
            consommations: Liste d'objets Consommation
            configJournee_matin: ConfigJournee pour le matin (heureDebut, heureFin, rendement)
            configJournee_apres: ConfigJournee pour l'après-midi (heureDebut, heureFin, rendement)
            heureChargeDebut: Heure début charge batterie (str "HH:MM:SS")
            heureChargeFin: Heure fin charge batterie (str "HH:MM:SS")
            capaciteBatterie: Capacité batterie en Wh
        
        Returns:
            dict: Dictionnaire avec besoins pour chaque période
        """
        try:
            print("\n📊 CALCUL DES BESOINS PAR PÉRIODE\n")
            
            # Calculer la puissance de charge batterie
            delta_minutes = (datetime.strptime(heureChargeFin, "%H:%M:%S") - 
                           datetime.strptime(heureChargeDebut, "%H:%M:%S")).total_seconds() / 60
            delta_heures = delta_minutes / 60
            puissance_charge = capaciteBatterie / delta_heures if delta_heures > 0 else 0
            
            # ============================================================
            # 1. BESOIN MATIN: Appareils (période entière) + Batterie (fenêtre charge)
            # ============================================================
            print("=" * 70)
            print("🌅 PÉRIODE MATIN")
            print("=" * 70)
            print(f"\nPériode: {configJournee_matin.heureDebut} → {configJournee_matin.heureFin}")
            print(f"Charge batterie: {heureChargeDebut} → {heureChargeFin}")
            
            # Besoin 1: Appareils uniquement durant toute la période matin
            resultat_appareils_matin = self.calculerPuissancePanneauRequise(
                consommations,
                configJournee_matin.heureDebut.strftime("%H:%M:%S") if hasattr(configJournee_matin.heureDebut, 'strftime') 
                else str(configJournee_matin.heureDebut),
                configJournee_matin.heureFin.strftime("%H:%M:%S") if hasattr(configJournee_matin.heureFin, 'strftime')
                else str(configJournee_matin.heureFin)
            )
            puissance_appareils_matin = resultat_appareils_matin['puissance_max']
            
            # Besoin 2: Appareils + Batterie durant la fenêtre de charge
            resultat_appareils_charge = self.calculerPuissancePanneauRequise(
                consommations,
                heureChargeDebut,
                heureChargeFin
            )
            puissance_appareils_charge = resultat_appareils_charge['puissance_max']
            puissance_appareils_batterie = puissance_appareils_charge + puissance_charge
            
            # Le besoin du matin = MAX(appareils seuls, appareils + batterie)
            besoin_matin_pratique = max(puissance_appareils_matin, puissance_appareils_batterie)
            
            print(f"\n✓ Puissance appareils période matin: {puissance_appareils_matin:.2f}W")
            print(f"✓ Puissance appareils + batterie (fenêtre charge): {puissance_appareils_batterie:.2f}W")
            print(f"✓ Besoin matin (pratique): {besoin_matin_pratique:.2f}W")
            
            # ============================================================
            # 2. BESOIN APRÈS-MIDI: Appareils seulement
            # ============================================================
            print("\n" + "=" * 70)
            print("🌤️  PÉRIODE FIN D'APRÈS-MIDI")
            print("=" * 70)
            print(f"\nPériode: {configJournee_apres.heureDebut} → {configJournee_apres.heureFin}")
            
            resultat_apres = self.calculerPuissancePanneauRequise(
                consommations,
                configJournee_apres.heureDebut.strftime("%H:%M:%S") if hasattr(configJournee_apres.heureDebut, 'strftime')
                else str(configJournee_apres.heureDebut),
                configJournee_apres.heureFin.strftime("%H:%M:%S") if hasattr(configJournee_apres.heureFin, 'strftime')
                else str(configJournee_apres.heureFin)
            )
            
            besoin_apres_pratique = resultat_apres['puissance_max']
            print(f"\n✓ Besoin fin d'après-midi (pratique): {besoin_apres_pratique:.2f}W (appareils seuls)")
            
            # ============================================================
            # 3. BESOIN SOIR: Batterie décharge
            # ============================================================
            print("\n" + "=" * 70)
            print("🌙 PÉRIODE SOIR")
            print("=" * 70)
            
            print(f"\n✓ Batterie décharge durant cette période")
            print(f"  Capacité: {capaciteBatterie:.2f} Wh")
            
            return {
                'besoin_matin_pratique': besoin_matin_pratique,
                'besoin_apres_pratique': besoin_apres_pratique,
                'puissance_charge_batterie': puissance_charge,
                'details': {
                    'matin': resultat_appareils_matin['details'],
                    'apres': resultat_apres['details']
                }
            }
            
        except Exception as e:
            print(f"✗ Erreur lors du calcul des besoins: {e}")
            import traceback
            traceback.print_exc()
            return {
                'besoin_matin_pratique': 0,
                'besoin_apres_pratique': 0,
                'puissance_charge_batterie': 0,
                'details': None
            }
    
    def calculerPuissancePratiquePanneau(self, besoin_matin, besoin_apres):
        """
        Détermine la puissance pratique (utilisable) finale du panneau
        en fonction des besoins du matin et de l'après-midi.
        
        Logique:
        1. Si besoin_apres > besoin_matin × 50%: Il manque de puissance
        2. Manque = besoin_apres - (besoin_matin × 50%)
        3. Manque convertir = Manque × 2 (inverse des 50%)
        4. Puissance pratique finale = besoin_matin + Manque convertir
        
        Args:
            besoin_matin: Besoin pratique matin en W
            besoin_apres: Besoin pratique après-midi en W
        
        Returns:
            dict: Puissance pratique et détails du calcul
        """
        try:
            print("\n" + "=" * 70)
            print("⚡ CALCUL DE LA PUISSANCE PRATIQUE DU PANNEAU")
            print("=" * 70)
            
            print(f"\nBesoin matin: {besoin_matin:.2f}W (appareils + batterie)")
            print(f"Besoin après-midi: {besoin_apres:.2f}W (appareils seuls)")
            
            # Vérifier si la puissance du matin à 50% suffit
            puissance_disponible_apres = besoin_matin * 0.50
            print(f"\n50% de la puissance matin: {puissance_disponible_apres:.2f}W")
            
            if besoin_apres <= puissance_disponible_apres:
                # 50% suffit, pas besoin d'augmenter
                puissance_pratique_finale = besoin_matin
                print(f"✓ 50% du matin >= après-midi")
                print(f"  {puissance_disponible_apres:.2f}W >= {besoin_apres:.2f}W")
                print(f"→ Puissance pratique finale: {puissance_pratique_finale:.2f}W")
                
                return {
                    'puissance_pratique': puissance_pratique_finale,
                    'logique': f"50% du matin suffit ({puissance_disponible_apres:.2f}W >= {besoin_apres:.2f}W)",
                    'manque': 0
                }
            else:
                # Manque de puissance
                manque = besoin_apres - puissance_disponible_apres
                manque_convertir = manque * 2  # Inverse des 50%
                puissance_pratique_finale = besoin_matin + manque_convertir
                
                print(f"✗ 50% du matin < après-midi")
                print(f"  {puissance_disponible_apres:.2f}W < {besoin_apres:.2f}W")
                print(f"\nManque: {besoin_apres:.2f}W - {puissance_disponible_apres:.2f}W = {manque:.2f}W")
                print(f"Convertir en théorique (÷ 0.50): {manque:.2f}W × 2 = {manque_convertir:.2f}W")
                print(f"→ Puissance pratique finale: {besoin_matin:.2f}W + {manque_convertir:.2f}W = {puissance_pratique_finale:.2f}W")
                
                return {
                    'puissance_pratique': puissance_pratique_finale,
                    'logique': f"Besoin supplémentaire de {manque_convertir:.2f}W",
                    'manque': manque_convertir
                }
                
        except Exception as e:
            print(f"✗ Erreur lors du calcul: {e}")
            return {
                'puissance_pratique': besoin_matin,
                'logique': "Erreur",
                'manque': 0
            }
    
    def calculerPuissanceTheoriquePanneau(self, puissance_pratique, rendement_matin):
        """
        Convertit la puissance pratique (utilisable) en puissance théorique
        qu'il faut ACHETER pour le panneau.
        
        Formule:
        Puissance théorique = Puissance pratique / (Rendement / 100)
        
        Args:
            puissance_pratique: Puissance utilizable en W
            rendement_matin: Rendement du matin en % (40 = 40%)
        
        Returns:
            dict: Puissance théorique et rendement
        """
        try:
            print("\n" + "=" * 70)
            print("☀️  CALCUL DE LA PUISSANCE THÉORIQUE DU PANNEAU À ACHETER")
            print("=" * 70)
            
            rendement_decimal = rendement_matin / 100
            puissance_theorique = puissance_pratique / rendement_decimal
            
            print(f"\nFormule: P_théorique = P_pratique / (Rendement / 100)")
            print(f"P_théorique = {puissance_pratique:.2f}W / {rendement_decimal:.2f}")
            print(f"P_théorique = {puissance_theorique:.2f}W")
            
            print(f"\n✓ Panneau à acheter: {puissance_theorique:.2f}W théorique")
            print(f"  Qui produit réellement: {puissance_theorique * rendement_decimal:.2f}W (à {rendement_matin}%)")
            
            return {
                'puissance_theorique': puissance_theorique,
                'puissance_pratique': puissance_pratique,
                'rendement': rendement_matin
            }
            
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return {
                'puissance_theorique': 0,
                'puissance_pratique': puissance_pratique,
                'rendement': rendement_matin
            }    
    def calculerPuissanceTheoriqueBatterie(self, puissance_pratique, marge=0.50):
        """
        Calcule la puissance théorique (capacité à acheter) de la batterie.
        
        Contrairement au panneau, la batterie utilise une marge de sécurité
        pour assurer durabilité et cycle de vie optimal.
        
        Formule:
        Puissance théorique = Puissance pratique × (1 + Marge)
        
        Exemple avec 50% de marge:
        - Puissance pratique: 240W
        - Marge: 50% (0.50)
        - P_théorique = 240W × (1 + 0.50) = 240W × 1.50 = 360W
        
        Args:
            puissance_pratique: Puissance utilisable de la batterie en W
            marge: Marge de sécurité en décimal (0.50 = 50%, 0.30 = 30%, etc.)
        
        Returns:
            dict: Puissance théorique et détails
        """
        try:
            print("\n" + "=" * 70)
            print("🔋 CALCUL DE LA PUISSANCE THÉORIQUE DE LA BATTERIE À ACHETER")
            print("=" * 70)
            
            puissance_theorique = puissance_pratique * (1 + marge)
            marge_nominale = puissance_pratique * marge
            
            print(f"\nFormule: P_théorique = P_pratique × (1 + Marge)")
            print(f"P_théorique = {puissance_pratique:.2f}W × (1 + {marge:.2f})")
            print(f"P_théorique = {puissance_pratique:.2f}W × {1 + marge:.2f}")
            print(f"P_théorique = {puissance_theorique:.2f}W")
            
            print(f"\n✓ Batterie à acheter: {puissance_theorique:.2f}W théorique")
            print(f"  Puissance utilisable: {puissance_pratique:.2f}W")
            print(f"  Marge de sécurité: {marge_nominale:.2f}W ({marge*100:.0f}%)")
            
            return {
                'puissance_theorique': puissance_theorique,
                'puissance_pratique': puissance_pratique,
                'marge': marge,
                'marge_nominale': marge_nominale
            }
            
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return {
                'puissance_theorique': puissance_pratique,
                'puissance_pratique': puissance_pratique,
                'marge': marge,
                'marge_nominale': 0
            }    
    def dimensionnerSystemeSolaire(self, consommations, configJournee_matin, configJournee_apres,
                                    heureChargeDebut, heureChargeFin, capaciteBatterie, marge_batterie=0.50):
        """
        FONCTION ORCHESTRATRICE - Calcule le dimensionnement complet du système solaire.
        
        Elle utilise les 4 fonctions précédentes pour:
        1. Calculer les besoins pratiques de chaque période
        2. Déterminer la puissance pratique finale du panneau
        3. Convertir en puissance théorique du panneau à acheter
        4. Calculer la puissance théorique de la batterie avec marge
        3. Convertir en puissance théorique à acheter
        
        Args:
            consommations: Liste d'objets Consommation
            configJournee_matin: ConfigJournee pour le matin (avec heureDebut, heureFin, rendement)
            configJournee_apres: ConfigJournee pour l'après-midi (avec heureDebut, heureFin, rendement)
            heureChargeDebut: Heure début charge batterie (str "HH:MM:SS")
            heureChargeFin: Heure fin charge batterie (str "HH:MM:SS")
            capaciteBatterie: Capacité batterie en Wh (puissance pratique)
            marge_batterie: Marge de sécurité batterie (0.50 = 50%, configurable)
        
        Returns:
            dict: Dimensionnement complet du système
        """
        try:
            print("\n" + "🔋" * 35)
            print("DIMENSIONNEMENT COMPLET DU SYSTÈME SOLAIRE")
            print("🔋" * 35)
            
            # ÉTAPE 1: Calculer les besoins par période
            besoins = self.calculerBesoinsParPeriode(
                consommations,
                configJournee_matin,
                configJournee_apres,
                heureChargeDebut,
                heureChargeFin,
                capaciteBatterie
            )
            
            # ÉTAPE 2: Calculer la puissance pratique du panneau
            puissance_pratique = self.calculerPuissancePratiquePanneau(
                besoins['besoin_matin_pratique'],
                besoins['besoin_apres_pratique']
            )
            
            # ÉTAPE 3: Calculer la puissance théorique
            puissance_theorique = self.calculerPuissanceTheoriquePanneau(
                puissance_pratique['puissance_pratique'],
                configJournee_matin.rendement
            )
            
            # ÉTAPE 4: Calculer la puissance théorique batterie
            puissance_batterie = self.calculerPuissanceTheoriqueBatterie(
                capaciteBatterie,
                marge_batterie
            )
            
            # RÉSUMÉ FINAL
            print("\n" + "=" * 70)
            print("📋 RÉSUMÉ DU DIMENSIONNEMENT")
            print("=" * 70)
            
            print("\n🔋 BATTERIE:")
            print(f"  Capacité requise: {capaciteBatterie:.2f} Wh")
            print(f"  Charge: {heureChargeDebut} → {heureChargeFin}")
            print(f"  Puissance charge: {besoins['puissance_charge_batterie']:.2f}W")
            print(f"  Puissance pratique: {capaciteBatterie:.2f}W")
            print(f"  Puissance théorique (à acheter): {puissance_batterie['puissance_theorique']:.2f}W")
            print(f"  Marge de sécurité: {puissance_batterie['marge_nominale']:.2f}W ({marge_batterie*100:.0f}%)")
            
            print("\n☀️  PANNEAU SOLAIRE:")
            print(f"  Puissance pratique (utilisable): {puissance_pratique['puissance_pratique']:.2f}W")
            print(f"  Puissance théorique (à acheter): {puissance_theorique['puissance_theorique']:.2f}W")
            print(f"  Rendement matin: {configJournee_matin.rendement:.0f}%")
            
            print("\n📊 COUVERTURE PAR PÉRIODE:")
            print(f"  Matin: {besoins['besoin_matin_pratique']:.2f}W (appareils + batterie)")
            print(f"  Après-midi: {besoins['besoin_apres_pratique']:.2f}W (appareils à 50% rendement)")
            print(f"  50% du panneau aux heures de pointe: {puissance_pratique['puissance_pratique'] * 0.5:.2f}W")
            
            if puissance_pratique['manque'] > 0:
                print(f"  ⚠️  Besoin supplémentaire: +{puissance_pratique['manque']:.2f}W")
            else:
                print(f"  ✓ Puissance suffisante")
            
            print("\n" + "=" * 70)
            
            return {
                'besoins': besoins,
                'puissance_pratique': puissance_pratique['puissance_pratique'],
                'puissance_theorique': puissance_theorique['puissance_theorique'],
                'batterie_capacite': capaciteBatterie,
                'batterie_puissance_pratique': capaciteBatterie,
                'batterie_puissance_theorique': puissance_batterie['puissance_theorique'],
                'batterie_marge': marge_batterie,
                'batterie_puissance_charge': besoins['puissance_charge_batterie'],
                'rendement_matin': configJournee_matin.rendement,
                'logique': puissance_pratique['logique']
            }
            
        except Exception as e:
            print(f"✗ Erreur lors du dimensionnement: {e}")
            import traceback
            traceback.print_exc()
            return None
