#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TEMPLATE pour corriger les imports dans les tests
Remplacez les 3-5 premières lignes de chaque fichier test par ceci:
"""

import sys
import os

# Ajouter les chemins PARENT (un niveau avant Tests/)
# Ceci doit être en PREMIER, avant tous les autres imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)  # Chemin parent pour tous les imports
sys.path.insert(0, os.path.join(parent_dir, 'Services'))
sys.path.insert(0, os.path.join(parent_dir, 'Models'))
sys.path.insert(0, os.path.join(parent_dir, 'Repositories'))
sys.path.insert(0, os.path.join(parent_dir, 'Database'))

# Maintenant vous pouvez importer les modules
from datetime import time, datetime
from ConsommationService import ConsommationService
from ChargeBatterieService import ChargeBatterieService
from Consommation import Consommation
from ConfigJournee import ConfigJournee
from Statut import Statut
# ... etc
