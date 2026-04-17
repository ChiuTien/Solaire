"""
Configuration d'exemple pour le dimensionnement solaire.
Ces valeurs peuvent être chargées dans l'interface graphique.
"""

# Configuration de la journée
CONFIG_JOURNEE = {
    "matin": {
        "heure_debut": "06:00:00",
        "heure_fin": "12:00:00",
        "rendement": 40,  # 40% le matin (soleil bas)
        "description": "Période de charge de la batterie"
    },
    "apres_midi": {
        "heure_debut": "12:00:00",
        "heure_fin": "18:00:00",
        "rendement": 100,  # 100% l'après-midi (soleil haut)
        "description": "Rendement optimal"
    },
    "soir": {
        "heure_debut": "18:00:00",
        "heure_fin": "22:00:00",
        "rendement": 0,  # 0% le soir (pas de soleil)
        "description": "Batterie décharge"
    }
}

# Configuration batterie
CONFIG_BATTERIE = {
    "charge_debut": "06:00:00",
    "charge_fin": "12:00:00",
    "capacite_wh": 500,  # En Watt-heure
    "marge_securite": 50,  # En pourcentage (50% = 0.50)
    "description": "Batterie 500 Wh avec 50% de marge"
}

# Appareils électriques d'exemple
APPAREILS_EXEMPLE_MAISON = [
    {
        "nom": "Réfrigérateur",
        "consommation_w": 150,
        "heure_debut": "06:00:00",
        "heure_fin": "22:00:00",
        "categorie": "cuisine",
        "note": "Fonctionne toute la journée"
    },
    {
        "nom": "Ventilateur",
        "consommation_w": 80,
        "heure_debut": "12:00:00",
        "heure_fin": "18:00:00",
        "categorie": "confort",
        "note": "Actif seulement l'après-midi"
    },
    {
        "nom": "Éclairage LED",
        "consommation_w": 60,
        "heure_debut": "18:00:00",
        "heure_fin": "22:00:00",
        "categorie": "eclairage",
        "note": "Éclairage soir/nuit"
    },
    {
        "nom": "Chauffe-eau électrique",
        "consommation_w": 1500,
        "heure_debut": "06:00:00",
        "heure_fin": "08:00:00",
        "categorie": "eau_chaude",
        "note": "Pic matin important"
    },
    {
        "nom": "Ordinateur",
        "consommation_w": 200,
        "heure_debut": "08:00:00",
        "heure_fin": "18:00:00",
        "categorie": "informatique",
        "note": "Travail de jour"
    }
]

APPAREILS_EXEMPLE_MINIMAL = [
    {
        "nom": "Réfrigérateur",
        "consommation_w": 150,
        "heure_debut": "06:00:00",
        "heure_fin": "22:00:00"
    },
    {
        "nom": "Éclairage",
        "consommation_w": 40,
        "heure_debut": "18:00:00",
        "heure_fin": "22:00:00"
    }
]

APPAREILS_EXEMPLE_COMPLET = [
    {"nom": "Réfrigérateur", "consommation_w": 150, "heure_debut": "06:00:00", "heure_fin": "22:00:00"},
    {"nom": "Machine à laver", "consommation_w": 1000, "heure_debut": "08:00:00", "heure_fin": "10:00:00"},
    {"nom": "Four électrique", "consommation_w": 2000, "heure_debut": "12:00:00", "heure_fin": "13:00:00"},
    {"nom": "Chauffe-eau", "consommation_w": 1500, "heure_debut": "06:00:00", "heure_fin": "08:00:00"},
    {"nom": "Ventilateur", "consommation_w": 80, "heure_debut": "12:00:00", "heure_fin": "18:00:00"},
    {"nom": "PC de bureau", "consommation_w": 200, "heure_debut": "08:00:00", "heure_fin": "18:00:00"},
    {"nom": "Téléviseur", "consommation_w": 100, "heure_debut": "19:00:00", "heure_fin": "22:00:00"},
    {"nom": "Micro-ondes", "consommation_w": 1000, "heure_debut": "12:30:00", "heure_fin": "13:00:00"},
]

# Profils solaires selon la géographie
PROFILS_SOLAIRES = {
    "tropical": {
        "description": "Zone tropicale (rendement élevé toute l'année)",
        "matin": 50,
        "apres_midi": 100,
        "soir": 0,
    },
    "tempere_ete": {
        "description": "Zone tempérée été (jours longs)",
        "matin": 60,
        "apres_midi": 100,
        "soir": 30,
    },
    "tempere_hiver": {
        "description": "Zone tempérée hiver (jours courts)",
        "matin": 20,
        "apres_midi": 60,
        "soir": 0,
    },
    "montagne": {
        "description": "Zone montagne (rendement variable)",
        "matin": 35,
        "apres_midi": 90,
        "soir": 10,
    }
}

# Capacités batterie recommandées selon besoins
CAPACITES_BATTERIE_RECOMMANDEES = {
    "minimal": {
        "wh": 200,
        "usage": "Appareil unique (éclairage)",
        "marge": 40
    },
    "petit": {
        "wh": 300,
        "usage": "Chalet, refuge montagne",
        "marge": 40
    },
    "moyen": {
        "wh": 500,
        "usage": "Studio, petit appartement",
        "marge": 50
    },
    "grand": {
        "wh": 1000,
        "usage": "Maison, gîte",
        "marge": 50
    },
    "tres_grand": {
        "wh": 2000,
        "usage": "Famille nombreuse, commerce",
        "marge": 60
    }
}


def get_exemple(nom: str) -> dict:
    """
    Récupère un exemple de configuration.
    
    Args:
        nom: "maison", "minimal", "complet"
    
    Returns:
        dict: Configuration d'appareils
    """
    exemples = {
        "maison": APPAREILS_EXEMPLE_MAISON,
        "minimal": APPAREILS_EXEMPLE_MINIMAL,
        "complet": APPAREILS_EXEMPLE_COMPLET,
    }
    return exemples.get(nom, APPAREILS_EXEMPLE_MAISON)


def get_profil_solaire(nom: str) -> dict:
    """
    Récupère un profil solaire.
    
    Args:
        nom: "tropical", "tempere_ete", "tempere_hiver", "montagne"
    
    Returns:
        dict: Profil solaire avec rendements
    """
    return PROFILS_SOLAIRES.get(nom, PROFILS_SOLAIRES["tempere_ete"])


def get_capacite_recommandee(nom: str) -> dict:
    """
    Récupère une capacité batterie recommandée.
    
    Args:
        nom: "minimal", "petit", "moyen", "grand", "tres_grand"
    
    Returns:
        dict: Capacité recommandée
    """
    return CAPACITES_BATTERIE_RECOMMANDEES.get(nom, CAPACITES_BATTERIE_RECOMMANDEES["moyen"])


if __name__ == "__main__":
    print("=== Configuration d'exemple ===\n")
    print("Configuration journée:")
    for period, config in CONFIG_JOURNEE.items():
        print(f"\n{period.upper()}:")
        print(f"  Heures: {config['heure_debut']} → {config['heure_fin']}")
        print(f"  Rendement: {config['rendement']}%")
    
    print(f"\n\nConfiguration Batterie:")
    print(f"  Capacité: {CONFIG_BATTERIE['capacite_wh']} Wh")
    print(f"  Charge: {CONFIG_BATTERIE['charge_debut']} → {CONFIG_BATTERIE['charge_fin']}")
    print(f"  Marge sécurité: {CONFIG_BATTERIE['marge_securite']}%")
    
    print(f"\n\nAppareils d'exemple (Maison):")
    total_w = 0
    for idx, app in enumerate(APPAREILS_EXEMPLE_MAISON, 1):
        print(f"\n{idx}. {app['nom']}")
        print(f"   Consommation: {app['consommation_w']}W")
        print(f"   Horaires: {app['heure_debut']} → {app['heure_fin']}")
        if app.get('categorie'):
            print(f"   Catégorie: {app['categorie']}")
        total_w += app['consommation_w']
    
    print(f"\n\nConsommation totale (peaks simultanés): {total_w}W")
    print(f"\nExemples disponibles: maison, minimal, complet")
    print(f"Profils solaires: tropical, tempere_ete, tempere_hiver, montagne")
