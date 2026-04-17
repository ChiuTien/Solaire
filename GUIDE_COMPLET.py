#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🔋 GUIDE COMPLET - Interface Graphique Dimensionnement Solaire

Ce fichier documente toute l'interface et comment l'utiliser.
"""

print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  ⚡ INTERFACE GRAPHIQUE - DIMENSIONNEMENT SYSTÈME SOLAIRE ⚡        ║
║                                                                      ║
║  Version: 1.0                                                        ║
║  Date: Avril 2026                                                    ║
║  Langage: Python 3.8+                                                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════
📋 TABLE DES MATIÈRES
═══════════════════════════════════════════════════════════════════════

1. ✅ REQUIREMENTS & INSTALLATION
2. 🚀 DÉMARRER L'APPLICATION
3. 📊 INTERFACE PRINCIPALE (3 onglets)
4. 📖 GUIDE DÉTAILLÉ PAR SECTION
5. 📝 EXEMPLES PRATIQUES
6. ⚙️ CONFIGURATION ADVANCÉE
7. 🆘 DÉPANNAGE

═══════════════════════════════════════════════════════════════════════
1️⃣ REQUIREMENTS & INSTALLATION
═══════════════════════════════════════════════════════════════════════

PRÉREQUIS SYSTÈME:
  • Python 3.8 ou plus récent
  • tkinter (inclus par défaut)
  • Environ 50 Mo d'espace disque

VÉRIFIER LES DÉPENDANCES:

  $ python3 --version
  Python 3.9.x

  $ python3 -c "import tkinter; print('✓ tkinter OK')"
  ✓ tkinter OK

INSTALLATION TKINTER:

  Linux (Ubuntu/Debian):
    $ sudo apt-get update
    $ sudo apt-get install python3-tk

  Linux (Fedora):
    $ sudo dnf install python3-tkinter

  macOS:
    $ brew install python-tk

  Windows:
    (Inclus avec Python.org installer - vérifier "tcl/tk")

═══════════════════════════════════════════════════════════════════════
2️⃣ DÉMARRER L'APPLICATION
═══════════════════════════════════════════════════════════════════════

OPTION 1: Lancer directement
  $ cd "/chemin/vers/Solaire"
  $ python Interface.py

OPTION 2: Script de lancement
  $ python run_interface.py

OPTION 3: Tester d'abord (recommandé)
  $ python test_interface.py
  
  Cela exécutera les tests et confirmera que tout fonctionne.
  
L'interface s'affichera avec:
  • Fenêtre 1400x900 pixels
  • 3 onglets de navigation
  • Boutons d'action en bas

═══════════════════════════════════════════════════════════════════════
3️⃣ INTERFACE PRINCIPALE - LES 3 ONGLETS
═══════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│ ONGLET 1: 📅 CONFIGURATION JOURNÉE                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ⚙️ Configure les 3 périodes de la journée et la batterie            │
│                                                                     │
│ SECTIONS:                                                           │
│  1. 🌅 MATIN (e.g. 06:00-12:00)                                     │
│     • Heure début                                                   │
│     • Heure fin                                                     │
│     • Rendement (%)                                                 │
│                                                                     │
│  2. ☀️ FIN D'APRÈS-MIDI (e.g. 12:00-18:00)                          │
│     • Heure début                                                   │
│     • Heure fin                                                     │
│     • Rendement (%)                                                 │
│                                                                     │
│  3. 🌙 SOIR (e.g. 18:00-22:00)                                      │
│     • Heure début                                                   │
│     • Heure fin                                                     │
│     • Rendement (%) → généralement 0                                │
│                                                                     │
│  4. 🔋 BATTERIE                                                     │
│     • Heure début charge (e.g. 06:00:00)                            │
│     • Heure fin charge (e.g. 12:00:00)                              │
│     • Capacité (Wh) - Par défaut: 500                               │
│     • Marge sécurité (%) - Par défaut: 50                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ ONGLET 2: ⚙️ APPAREILS ÉLECTRIQUES                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📝 Ajoutez et gérez vos appareils électriques                       │
│                                                                     │
│ SECTION AJOUT:                                                      │
│  • Nom Appareil (ex: "Réfrigérateur")                               │
│  • Consommation (W) (ex: 150)                                       │
│  • Heure Début (HH:MM:SS) (ex: "06:00:00")                          │
│  • Heure Fin (HH:MM:SS) (ex: "22:00:00")                            │
│  • Bouton: [Ajouter]                                                │
│                                                                     │
│ SECTION LISTE:                                                      │
│  • Tableau affichant tous les appareils ajoutés                     │
│  • Sélectionnez pour supprimer                                      │
│  • Boutons: [Supprimer Sélectionné] [Supprimer Tous]                │
│                                                                     │
│ EXEMPLE D'AJOUT:                                                    │
│  Nom: Réfrigérateur                                                 │
│  Consommation: 150                                                  │
│  Début: 06:00:00                                                    │
│  Fin: 22:00:00                                                      │
│  → [Ajouter]                                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ ONGLET 3: 📊 RÉSULTATS                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📈 Affiche les résultats du dimensionnement                         │
│                                                                     │
│ SECTIONS DE RÉSULTATS:                                              │
│  1. 🔋 BATTERIE                                                     │
│     • Capacité requise (Wh)                                         │
│     • Puissance pratique (W) - Utilisable                           │
│     • Puissance théorique (W) - À acheter                           │
│     • Marge de sécurité (%)                                         │
│     • Puissance de charge (W)                                       │
│                                                                     │
│  2. ☀️ PANNEAU SOLAIRE                                              │
│     • Puissance pratique (utilisable) (W)                           │
│     • Puissance théorique (à acheter) (W)                           │
│     • Rendement matin (%)                                           │
│     • Pic puissance matin (W)                                       │
│                                                                     │
│  3. 📊 COUVERTURE PAR PÉRIODE                                       │
│     • Matin (appareils + batterie) (W)                              │
│     • Après-midi (appareils seuls) (W)                              │
│                                                                     │
│  4. ✓ NOTATION                                                      │
│     • Logique du calcul                                             │
│     • Suffisant ou insuffisant                                      │
│                                                                     │
│ 💡 INTERPRÉTATION:                                                  │
│  "Puissance théorique" = Ce que vous devez ACHETER                  │
│  "Puissance pratique" = Ce que vous utiliserez réellement           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════
4️⃣ GUIDE DÉTAILLÉ PAR SECTION
═══════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────────
4.1 CONFIGURATION JOURNÉE - PARAMÈTRES CLÉS
──────────────────────────────────────────────────────────────────────

FORMAT DES HEURES:
  Format accepté: HH:MM:SS (24 heures)
  Exemples valides:
    ✓ 06:00:00 (6 heures du matin)
    ✓ 12:30:45 (12h30 45 secondes)
    ✓ 23:59:59 (une seconde avant minuit)
  
  Exemples invalides:
    ✗ 6:00:00 (manque le 0)
    ✗ 06:00 (pas de secondes)
    ✗ 06h00m00s (format français)

RENDEMENT (%):
  • Matin: 30-50% (soleil bas)
    ↳ Plus bas = soleil plus bas
    ↳ Exemple: 6h→12h ➜ 40%
  
  • Après-midi: 80-100% (soleil haut)
    ↳ 100% = conditions optimales
    ↳ Exemple: 12h→18h ➜ 100%
  
  • Soir: 0-20% (crépuscule/nuit)
    ↳ 0% si pas de soleil du tout
    ↳ Exemple: 18h→22h ➜ 0%

BATTERIE - PLAGE DE CHARGE:
  • Début: Quand le soleil se lève ou apparaît
  • Fin: Avant les pics de consommation importants
  • Exemple: 06:00:00 → 12:00:00
  • ⚠️ Doit être pendant heures avec soleil!

CAPACITÉ BATTERIE (Wh):
  • Wh = Watt-heure (unité d'énergie)
  • 500 Wh = 500W une heure, ou 250W deux heures
  
  Recommandations:
    À partir de  Wh | Usage
    ─────────────────┼────────────────────────
    200             | Éclairage seul
    300-500         | Petit usage (chalet)
    500-1000        | Maison moyenne
    1000-2000       | Maison grande/commerce
    2000+           | Installation commerciale

MARGE SÉCURITÉ BATTERIE (%):
  • Marge = Capacité supplémentaire au-delà du besoin
  • 50% = acheter 1.5x la capacité requise
  • Assure durabilité et cycles de charge
  
  Recommandations:
    Marge | Durée de vie | Usage
    ──────┼──────────────┼──────────────────
    30%   | 3-5 ans      | Tight budget
    50%   | 5-8 ans      | Recommandé
    60%   | 8-10 ans     | Premium
    70%+  | 10+ ans      | Professionnel

──────────────────────────────────────────────────────────────────────
4.2 APPAREILS ÉLECTRIQUES - VALEURS TYPIQUES
──────────────────────────────────────────────────────────────────────

APPAREILS DE CUISINE:
  Réfrigérateur         | 100-150W  | 24h
  Congélateur          | 100-200W  | 24h
  Micro-ondes          | 800-1500W | 5-10 min
  Four électrique       | 1500-3000W| 30-60 min
  Machine à laver       | 500-1000W | 1-2h
  Lave-vaisselle        | 1200-2000W| 2-3h
  Bouilloire            | 1500-2000W| 5 min

APPAREILS DE CONFORT:
  Ventilateur           | 50-100W   | 4-8h
  Climatiseur           | 1000-2000W| 8h
  Chauffe-eau élec.     | 1500-2000W| 1-2h
  Radiateur électrique  | 1000-2000W| 4-8h

APPAREILS INFORMATIQUES:
  Ordinateur portable   | 50-100W   | 8h
  PC de bureau          | 150-300W  | 8h
  Imprimante            | 20-50W    | 1h
  Routeur WiFi          | 10-20W    | 24h

ÉCLAIRAGE:
  Ampoule LED           | 5-15W     | 5-8h
  Ampoule halogène      | 50-100W   | 5-8h
  Lampe de bureau       | 20-40W    | 5h

DIVERTISSEMENT:
  Téléviseur            | 100-200W  | 4-6h
  Enceinte audio        | 50-200W   | 4-6h

──────────────────────────────────────────────────────────────────────
4.3 INTERPRÉTATION DES RÉSULTATS
──────────────────────────────────────────────────────────────────────

🔋 BATTERIE:

  Puissance pratique:
    → Ce que vous développerez réellement
    → Pour notre exemple: 500W
    → C'est votre besoin réel en Wh

  Puissance théorique (à acheter):
    → Size du produit à commander
    → = Puissance pratique × (1 + Marge)
    → Pour notre exemple: 500W × 1.50 = 750W
    → Vous achèterez une batterie 750 Wh

☀️ PANNEAU SOLAIRE:

  Puissance pratique:
    → Energy que le panneau produit réellement
    → À 40% rendement matin
    → Pour notre exemple: 1733W

  Puissance théorique (à acheter):
    → Spécification du panneau à commander
    → = Puissance pratique / (Rendement%)
    → Pour notre exemple: 1733 / 0.40 = 4333W
    → Vous achèterez un panneau spécification 4333W

PIC PUISSANCE MATIN:
  → Consommation maximale simultanée le matin
  → Aide à dimensionner le régulateur de charge
  → Pour notre exemple: 1733W

═══════════════════════════════════════════════════════════════════════
5️⃣ EXEMPLES PRATIQUES
═══════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────────
EXEMPLE 1: CHALET SIMPLE (Minimal)
──────────────────────────────────────────────────────────────────────

📋 CONFIGURATION JOURNÉE:

  Matin (06:00 - 12:00, 40%)
  Après-midi (12:00 - 18:00, 100%)
  Soir (18:00 - 22:00, 0%)
  Batterie: 06:00 → 12:00, 300 Wh, 50% marge

⚙️ APPAREILS:

  1. Réfrigérateur    | 150W  | 06:00 - 22:00
  2. Éclairage        | 40W   | 18:00 - 22:00

📊 RÉSULTATS ATTENDUS:

  🔋 Batterie:
     • Puissance pratique: ~300W
     • Puissance théorique: ~450W (à acheter)
  
  ☀️ Panneau:
     • Puissance pratique: ~300W
     • Puissance théorique: ~750W (à acheter)

💡 INTERPRÉTATION:

  Batterie à acheter: 450 Wh (e.g. batterie LiFePO4 48V 100Ah)
  Panneau à acheter: 750W (e.g. panneau monocristallin 750W)

──────────────────────────────────────────────────────────────────────
EXEMPLE 2: MAISON COMPLÈTE
──────────────────────────────────────────────────────────────────────

📋 CONFIGURATION JOURNÉE:

  Matin (06:00 - 12:00, 40%)
  Après-midi (12:00 - 18:00, 100%)
  Soir (18:00 - 22:00, 0%)
  Batterie: 06:00 → 12:00, 500 Wh, 50% marge

⚙️ APPAREILS:

  1. Réfrigérateur      | 150W | 06:00 - 22:00
  2. Machine à laver    | 800W | 08:00 - 10:00
  3. Four électrique    |1500W | 12:00 - 13:00
  4. Chauffe-eau        |1500W | 06:00 - 08:00
  5. Ventilateur        |  80W | 12:00 - 18:00
  6. PC de bureau       | 200W | 08:00 - 18:00
  7. Télévision         | 100W | 19:00 - 22:00
  8. Micro-ondes        |1000W | 12:30 - 13:00

📊 RÉSULTATS ATTENDUS:

  🔋 Batterie:
     • Puissance pratique: ~500W
     • Puissance théorique: ~750W
  
  ☀️ Panneau:
     • Puissance pratique: ~1733W
     • Puissance théorique: ~4333W
  
  Pic matin: ~1733W

💡 INTERPRÉTATION:

  Batterie: 750 Wh (LiFePO4 compatible)
  Panneau: 4.3 kW (configuration 3-4 panneaux 1.2kW)
  Régulateur: ≥2000W

═══════════════════════════════════════════════════════════════════════
6️⃣ CONFIGURATION ADVANCÉE
═══════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────────
Charger des exemples de config_exemple.py:
──────────────────────────────────────────────────────────────────────

  from config_exemple import (
      APPAREILS_EXEMPLE_MAISON,
      PROFILS_SOLAIRES,
      CAPACITES_BATTERIE_RECOMMANDEES
  )

──────────────────────────────────────────────────────────────────────
Personnaliser l'interface:
──────────────────────────────────────────────────────────────────────

  1. Modifier les valeurs par défaut dans Interface.py
  2. Changer les couleurs (color_header, color_accent, etc.)
  3. Ajouter des champs supplémentaires dans les frames

═══════════════════════════════════════════════════════════════════════
7️⃣ DÉPANNAGE
═══════════════════════════════════════════════════════════════════════

❌ PROBLÈME: "Format d'heure invalide"
✓ SOLUTION:
  • Utilisez le format exact HH:MM:SS
  • Vérifiez les 0 devant (06 pas 6)
  • Exemples: 06:00:00, 12:30:45, 23:59:59

❌ PROBLÈME: "Veuillez ajouter au moins un appareil"
✓ SOLUTION:
  • Allez dans l'onglet "Appareils Électriques"
  • Remplissez tous les champs
  • Cliquez "Ajouter"
  • Vérifiez que l'appareil apparaît dans la liste

❌ PROBLÈME: "Valeur invalide"
✓ SOLUTION:
  • Consommation: nombre entier ou décimal (150 ou 150.5)
  • Pas de virgule française (150,5 ✗)
  • Rendement: nombre 0-100

❌ PROBLÈME: L'interface ne démarre pas
✓ SOLUTION:
  • Vérifiez tkinter: python3 -c "import tkinter"
  • Installez si nécessaire (voir section 1)
  • Vérifiez le chemin: cd /home/chiu/Documents/ITU/L2/S4/Projet\ Tahina/Exo/Solaire

❌ PROBLÈME: "Erreur lors du calcul"
✓ SOLUTION:
  • Vérifiez tous les champs sont remplis
  • Vérifiez format des heures (HH:MM:SS)
  • Heures début < heures fin?
  • Consommations > 0?

❌ PROBLÈME: Résultats semblent incorrects
✓ SOLUTION:
  • Vérifiez les rendements (matin < après-midi)
  • Vérifiez les heures des appareils
  • Vérifiez la capacité batterie
  • Relancez le calcul

═══════════════════════════════════════════════════════════════════════
📚 FICHIERS ASSOCIÉS
═══════════════════════════════════════════════════════════════════════

Interface.py          → Interface graphique principale
run_interface.py      → Script de lancement
test_interface.py     → Tests fonctionnels
config_exemple.py     → Configurations d'exemple
README_GUI.md         → Documentation GUI
GUIDE.txt             → Ce fichier

═══════════════════════════════════════════════════════════════════════
🔗 RESSOURCES SUPPLÉMENTAIRES
═══════════════════════════════════════════════════════════════════════

Documentation SQL:     Sql/Table.sql, Sql/Base.sql
Modèles de données:    Models/
Services de calcul:    Services/ConsommationService.py
Tests existants:       Tests/

═══════════════════════════════════════════════════════════════════════
📞 SUPPORT
═══════════════════════════════════════════════════════════════════════

Pour toute question sur:
  • L'interface: Interface.py - classe SolaireGUI
  • Les calculs: Services/ConsommationService.py
  • La structure: Voir fichiers SQL pour le schéma
  • Les exemples: config_exemple.py

═══════════════════════════════════════════════════════════════════════

✓ Prêt à commencer! 

  Lancez: python Interface.py
  Ou tester d'abord: python test_interface.py

═══════════════════════════════════════════════════════════════════════
""")
