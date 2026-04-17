# 🔋 Interface Graphique - Dimensionnement Système Solaire

## Vue d'ensemble

Cette interface graphique permet de **dimensionner complètement un système solaire avec batterie** pour répondre aux besoins énergétiques sur une journée complète.

## Fonctionnalités

### 1. 📅 **Configuration Journée**
Configurez les trois périodes de votre journée :

- **🌅 MATIN** (ex: 06:00 - 12:00)
  - Rendement réduit (40-50%)
  - Énergies requises pour appareils + batterie en charge

- **☀️ FIN D'APRÈS-MIDI** (ex: 12:00 - 18:00)
  - Rendement optimal (100%)
  - Énergies requises pour appareils seuls

- **🌙 SOIR** (ex: 18:00 - 22:00)
  - Sans apport solaire
  - Batterie décharge pour les appareils

**Batterie:**
- Plage horaire de charge (ex: 06:00 - 12:00)
- Capacité en Wh (par défaut: 500 Wh)
- Marge de sécurité (par défaut: 50%)

### 2. ⚙️ **Appareils Électriques**
Ajoutez tous vos appareils électriques :

| Champ | Exemple | Format |
|-------|---------|--------|
| Nom | "Réfrigérateur" | Texte |
| Consommation | 150 | Watts (W) |
| Heure Début | "06:00:00" | HH:MM:SS |
| Heure Fin | "22:00:00" | HH:MM:SS |

**Exemple d'appareils types:**
- Réfrigérateur: 150W, 06:00-22:00
- Ventilateur: 80W, 12:00-18:00
- Lampes: 20W chacune, 18:00-22:00
- Chauffe-eau: 1500W, 06:00-08:00

### 3. 📊 **Résultats**
Les résultats affichent:

**🔋 BATTERIE**
- Capacité requise (Wh)
- Puissance pratique (W) - utilisable
- Puissance théorique (W) - à acheter avec marge
- Marge de sécurité (%)
- Puissance de charge (W)

**☀️ PANNEAU SOLAIRE**
- Puissance pratique (utilisable)
- Puissance théorique (à acheter)
- Rendement matin (%)
- Pic puissance matin (W)

**📊 COUVERTURE PAR PÉRIODE**
- Matin: appareils + batterie en charge
- Après-midi: appareils seuls (rendement 100%)

## Utilisation

### Lancer l'interface

```bash
python Interface.py
```

ou 

```bash
python run_interface.py
```

### Étapes d'utilisation

1. **Configurez votre journée** dans l'onglet "Configuration Journée"
   - Heures et rendements pour chaque période
   - Plage de charge batterie

2. **Ajoutez vos appareils** dans l'onglet "Appareils Électriques"
   - Cliquez "Ajouter" pour chaque appareil
   - Vérifiez la liste affichée

3. **Cliquez "CALCULER"** en bas
   - L'algorithme dimensionne votre système
   - Les résultats s'affichent dans l'onglet "Résultats"

4. **Consultez les résultats**
   - Batterie: puissance pratique vs théorique
   - Panneau: puissance pratique vs théorique
   - Pic de consommation matin

### Réinitialiser

- **"Réinitialiser"** - Efface tous les appareils et rémet les configurations par défaut
- **"Quitter"** - Ferme l'application

## Formats acceptés

### Heures
Format: `HH:MM:SS` (24 heures)
- Valide: "06:30:00", "14:15:30", "22:00:00"
- Invalide: "6:30:00", "14:15", "2:30 PM"

### Nombres
Format: Décimal avec point
- Valide: "1500", "150.5", "80.25"
- Invalide: "150,5", "1 500"

## Exemple complet

### Configuration Journée
```
Matin:
  - Heure début: 06:00:00
  - Heure fin: 12:00:00
  - Rendement: 40%

Après-midi:
  - Heure début: 12:00:00
  - Heure fin: 18:00:00
  - Rendement: 100%

Soir:
  - Heure début: 18:00:00
  - Heure fin: 22:00:00
  - Rendement: 0%

Batterie:
  - Charge: 06:00:00 → 12:00:00
  - Capacité: 500 Wh
  - Marge: 50%
```

### Appareils
```
1. Réfrigérateur: 150W, 06:00:00 → 22:00:00
2. Ventilateur: 80W, 12:00:00 → 18:00:00
3. Éclairage: 60W, 18:00:00 → 22:00:00
4. Chauffe-eau: 1500W, 06:00:00 → 08:00:00
```

### Résultats attendus
```
BATTERIE:
  - Puissance pratique: ~500W
  - Puissance théorique (à acheter): ~750W (avec 50% marge)

PANNEAU SOLAIRE:
  - Puissance pratique: ~1000W (exemple)
  - Puissance théorique (à acheter): ~2500W (à 40% rendement matin)
  - Pic matin: ~1000W
```

## Dépannage

### "Format d'heure invalide"
→ Utilisez le format `HH:MM:SS` exactement

### "Veuillez ajouter au moins un appareil"
→ Ajoutez au moins un appareil avant de calculer

### "Erreur lors du calcul"
→ Vérifiez que tous les champs sont remplis correctement
→ Vérifiez que les heures début sont antérieures aux heures fin

### Interface ne démarre pas
→ Vérifiez que tkinter est installé:
```bash
# Linux
sudo apt-get install python3-tk

# Tester
python3 -c "import tkinter; print('tkinter OK')"
```

## Structure des données

Les données sont conservées en mémoire pendant l'exécution. Pour persister les données :
- Utilisez les services dans `Services/`
- Connectez-vous à la base de données via `Database/Connexion.py`
- Utilisez les repositories dans `Repositories/`

## Architecture

```
Interface.py
├── SolaireGUI (classe principale)
├── create_config_tab() - Onglet Configuration
├── create_appareils_tab() - Onglet Appareils
├── create_resultats_tab() - Onglet Résultats
└── calculer() - Lance le dimensionnement via ConsommationService
```

## Notes importantes

⚠️ **Rendement:**
- Matin: Rendement réduit (le soleil est bas)
- Après-midi: Rendement optimal (le soleil est haut)
- Soir: Rendement 0% (pas de soleil)

⚠️ **Marge batterie:**
- Recommandé: 40-50%
- Assure la durabilité et le cycle de vie du matériel

⚠️ **Capacité batterie:**
- Doit couvrir l'énergie du soir et la réserve
- Rentrée en Wh (Watt-heure)

## Auteur
Interface créée pour le projet de dimensionnement solaire - Tahina

---

**Version:** 1.0  
**Date:** Avril 2026  
**Langage:** Python 3.8+
