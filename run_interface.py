#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script d'exemple pour démarrer l'interface GUI du système solaire.
Assurez-vous que tkinter est installé sur votre système.

Pour Linux:
    sudo apt-get install python3-tk

Pour macOS:
    Devrait être inclus avec Python

Pour Windows:
    Devrait être inclus avec Python
"""

import sys
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

from Interface import SolaireGUI
import tkinter as tk


def main():
    """Lance l'application GUI."""
    print("=" * 70)
    print("🔋 Bienvenue dans le dimensionneur de système solaire")
    print("=" * 70)
    print("\nLancement de l'interface graphique...\n")
    
    root = tk.Tk()
    app = SolaireGUI(root)
    
    print("✓ Interface chargée avec succès!")
    print("\nGuide d'utilisation:")
    print("1. Configurez les périodes de la journée (Configuration Journée)")
    print("   - Matin, Fin d'après-midi, Soir")
    print("   - Rentrez les heures et le rendement pour chaque période")
    print("\n2. Ajoutez vos appareils électriques (Appareils Électriques)")
    print("   - Nom de l'appareil")
    print("   - Consommation en Watts")
    print("   - Heures d'utilisation")
    print("\n3. Cliquez sur 'CALCULER' pour lancer le dimensionnement")
    print("\n4. Consultez les résultats (onglet Résultats)")
    print("   - Puissances théoriques et pratiques requises")
    print("   - Batterie et panneau solaire à acheter")
    print("   - Pic de consommation\n")
    
    root.mainloop()


if __name__ == "__main__":
    main()
