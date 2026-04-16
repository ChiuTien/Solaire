# Documentation 5: Explication des Fonctions de Calcul Solaire

## Vue d'ensemble

Ce document explique en détail toutes les fonctions créées dans les Services pour calculer les paramètres d'un système solaire (batterie + panneau).

---

## 📊 FONCTIONS CONSOMMATIONSERVICE

### 1. `calculerCapaciteBatterieRequise(consommations)`

**Objectif:** Déterminer la **capacité totale en Wh** (Watt-heures) qu'une batterie doit avoir pour supporter tous les appareils avec leurs chevauchements pendant une journée.

**Paramètres:**
- `consommations`: Liste d'objets Consommation avec (id, puissance, heureDebut, heureFin)

**Logique:**
1. Crée une liste d'**événements** (début et fin de chaque consommation)
2. Trie les événements par ordre chronologique
3. Divise la journée en **intervalles** entre chaque événement
4. Pour chaque intervalle, calcule:
   - Puissance active = somme de tous les appareils actifs
   - Durée de l'intervalle
   - Énergie Wh = Puissance × Durée
5. Somme toutes les énergies = **capacité totale**

**Formule:**
```
Énergie (Wh) = Puissance (W) × Temps (h)
Capacité totale = Σ(Puissance × Durée pour chaque intervalle)
```

**Retour:**
```python
{
    'capacite_totale': float,      # Wh (Watt-heures)
    'details': [                   # Détails par intervalle
        {
            'debut': str,          # "HH:MM:SS"
            'fin': str,            # "HH:MM:SS"
            'puissance': float,    # W (somme appareils actifs)
            'temps_heures': float, # Durée en heures
            'energie_wh': float    # Énergie Wh pour cet intervalle
        }
    ]
}
```

**Exemple:**
```
Consommations:
- C1: 70W de 22:00 à 00:00
- C2: 100W de 22:00 à 23:00

Intervalles:
- 22:00-23:00: (70+100)W = 170W × 1h = 170 Wh
- 23:00-00:00: 70W × 1h = 70 Wh

Capacité totale = 170 + 70 = 240 Wh
```

**Cas spéciaux:**
- Gère les **traversées de minuit** (ex: 22:00 → 02:00)
- Précision à la **minute** avec conversion en secondes

---

### 2. `calculerPuissanceMaxSimultanee(consommations)`

**Objectif:** Trouver la **puissance instantanée maximale** (peak power) requise quand le plus d'appareils fonctionnent simultanément.

**Paramètres:**
- `consommations`: Liste d'objets Consommation

**Logique:**
1. Crée une liste d'événements (début/fin de chaque appareil)
2. Trie chronologiquement
3. Parcourt les événements en gardant une somme de puissance active
4. Enregistre le **maximum** atteint

**Retour:**
```python
{
    'puissance_max': float,        # W (maximum instantané)
    'intervalle_max': {            # Quand ce max est atteint
        'debut': str,              # "HH:MM:SS"
        'fin': str,                # "HH:MM:SS"
        'puissance': float         # W
    },
    'details': [list]              # Tous les intervalles
}
```

**Exemple:**
```
C1: 70W de 22:00 à 24:00
C2: 100W de 22:00 à 23:00

Max = 170W (entre 22:00 et 23:00)
```

---

### 3. `calculerConsommationTotale(consommations)`

**Objectif:** Calculer l'**énergie totale consommée** par tous les appareils (sans chevauchement).

**Paramètres:**
- `consommations`: Liste d'objets Consommation

**Logique:**
1. Pour chaque consommation:
   - Énergie = Puissance × Durée
   - Accumule dans un total
2. Retourne le total

**Formule:**
```
Consommation totale = Σ(Puissance × Durée pour chaque appareil)
```

**Retour:** `float` en Wh

**Différence avec capaciteBatterie:**
- `calculerCapaciteBatterieRequise`: Considère les **chevauchements** (quand appareils fonctionnent ensemble)
- `calculerConsommationTotale`: Somme simple sans considérer les chevauchements

---

### 4. `calculerPuissancePanneauRequise(consommations, heureDebut, heureFin)`

**Objectif:** Déterminer la **puissance maximale du panneau** nécessaire durant un intervalle spécifique, en considérant les chevauchements d'appareils.

**Paramètres:**
- `consommations`: Liste d'objets Consommation
- `heureDebut`: str "HH:MM:SS" - début de l'intervalle d'analyse
- `heureFin`: str "HH:MM:SS" - fin de l'intervalle d'analyse

**Logique:**
1. Filtre les appareils qui **chevauchent** l'intervalle [heureDebut, heureFin]
2. Divise l'intervalle en sous-intervalles basés sur les événements des appareils
3. Pour chaque sous-intervalle, calcule la puissance totale active
4. Retourne le **maximum**

**Retour:**
```python
{
    'puissance_max': float,        # W (le max dans l'intervalle)
    'intervalle_max': {            # Où ce max est atteint
        'debut': str,              # "HH:MM:SS"
        'fin': str,                # "HH:MM:SS"
        'puissance': float         # W
    },
    'details': [list]              # Tous les sous-intervalles
}
```

**Exemple:**
```
Intervalle d'analyse: 10:00 → 14:00
Appareils:
- C1: 75W de 10:30 à 11:00
- C2: 100W de 10:00 à 13:00
- C3: 50W de 13:00 à 14:00

Sous-intervalles:
- 10:00-10:30: 100W (C2 seul)
- 10:30-11:00: 175W (C1 + C2) ← MAX
- 11:00-13:00: 100W (C2 seul)
- 13:00-14:00: 50W (C3 seul)

Puissance max = 175W
```

---

### 5. `calculerPuissanceTotalePanneau(consommations, heureDebut, heureFin, puissanceChargeBatterie, rendement=100)`

**Objectif:** Calculer la **puissance requise du panneau** pour alimenter les appareils ET charger la batterie simultanément, en tenant compte du **rendement**.

**Paramètres:**
- `consommations`: Liste d'objets Consommation
- `heureDebut`: str "HH:MM:SS" - intervalle d'analyse
- `heureFin`: str "HH:MM:SS"
- `puissanceChargeBatterie`: float (W) - puissance nécessaire pour charger batterie
- `rendement`: float (%) - rendement du panneau (0-100, défaut 100)

**Logique:**
1. Récupère puissance max appareils dans l'intervalle
2. Additionne avec puissance charge batterie
3. Divise par rendement pour obtenir puissance théorique

**Formules:**
```
Puissance requise = Max(appareils) + Puissance charge batterie
Puissance théorique = Puissance requise / (Rendement / 100)
```

**Retour:**
```python
{
    'puissance_requise': float,        # W (utilisable, pratique)
    'puissance_theorique': float,      # W (à acheter)
    'puissance_appareils': float,      # W (max appareils)
    'puissance_batterie': float,       # W (charge batterie)
    'rendement': float,                # % appliqué
    'details': dict                    # Détails complets
}
```

**Exemple:**
```
- Appareils max: 175W
- Charge batterie: 60W
- Puissance requise: 175W + 60W = 235W
- Rendement: 80%
- P théorique = 235W / 0.80 = 293.75W

Le panneau doit théoriquement faire 293.75W pour produire 235W utiles
```

---

### 6. `calculerBesoinsParPeriode(consommations, configJournee_matin, configJournee_apres, heureChargeDebut, heureChargeFin, capaciteBatterie)`

**Objectif:** Calculer les **besoins pratiques (utilisables)** pour chaque période de la journée (matin/après/soir).

**Paramètres:**
- `consommations`: Liste d'objets Consommation
- `configJournee_matin`: ConfigJournee (heureDebut, heureFin, rendement)
- `configJournee_apres`: ConfigJournee (pour fin d'après-midi)
- `heureChargeDebut`, `heureChargeFin`: str - fenêtre de charge batterie
- `capaciteBatterie`: float (Wh)

**Logique par période:**

**MATIN (P1):**
- Analyse la **période entière** (ex: 06:00-17:00) pour trouver tous les appareils
- Calcule:
  1. Puissance appareils pendant toute la P1
  2. Puissance appareils + batterie pendant fenêtre charge
- Besoin matin = MAX des deux
- Si appareil traverse 15:00-17:00, il est bien trouvé même s'il dépasse fenêtre charge

**FIN D'APRÈS (P2):**
- Analyse la **période entière** (ex: 17:00-19:00)
- Besoin = puissance appareils max dans P2

**SOIR (P3):**
- Batterie décharge seule
- Pas de panneau

**Retour:**
```python
{
    'besoin_matin_pratique': float,        # W (appareils ou appareils+batterie)
    'besoin_apres_pratique': float,        # W (appareils seuls)
    'puissance_charge_batterie': float,    # W (calculée)
    'details': dict                        # Détails par période
}
```

**⚠️ IMPORTANT: Gère les appareils qui traversent les limites entre périodes!**

---

### 7. `calculerPuissancePratiquePanneau(besoin_matin, besoin_apres)`

**Objectif:** Déterminer la **puissance pratique finale du panneau** en comparant les besoins du matin et de l'après-midi.

**Paramètres:**
- `besoin_matin`: float (W) - besoin pratique matin
- `besoin_apres`: float (W) - besoin pratique après-midi

**Logique:**
1. Calcule: 50% du matin = besoin_matin × 0.50 (après-midi = 50% rendement)
2. **Si** 50% matin ≥ besoin_après → Pas besoin d'augmenter
   - Puissance = besoin_matin
3. **Sinon** → Il manque de puissance
   - Manque = besoin_après - (besoin_matin × 0.50)
   - Manque convertir = Manque × 2 (inverse de 50%)
   - Puissance = besoin_matin + manque convertir

**Formule:**
```
Disponible après = Puissance matin × 0.50

Si Disponible ≥ Besoin après:
    P_pratique = Besoin matin

Sinon:
    Manque = Besoin après - Disponible
    P_pratique = Besoin matin + (Manque × 2)
```

**Retour:**
```python
{
    'puissance_pratique': float,       # W (utilisable)
    'logique': str,                    # Explication
    'manque': float                    # W supplémentaire si besoin
}
```

**Exemple:**
```
- Besoin matin: 235W
- Besoin après: 100W
- 50% du matin: 235 × 0.50 = 117.5W
- 117.5W ≥ 100W? OUI
- Puissance pratique = 235W
```

---

### 8. `calculerPuissanceTheoriquePanneau(puissance_pratique, rendement_matin)`

**Objectif:** Convertir la **puissance pratique en puissance théorique** (ce qu'on doit acheter).

**Paramètres:**
- `puissance_pratique`: float (W) - puissance utilisable
- `rendement_matin`: float (%) - rendement du matin

**Logique:**
```
P_théorique = P_pratique / (Rendement / 100)
```

**Exemple:**
```
- Puissance pratique: 235W
- Rendement: 40%
- P théorique = 235W / 0.40 = 587.50W

On achète 587.50W qui produit 235W en conditions réelles
```

**Retour:**
```python
{
    'puissance_theorique': float,      # W (à acheter)
    'puissance_pratique': float,       # W (utilisable)
    'rendement': float                 # % appliqué
}
```

---

### 9. `calculerPuissanceTheoriqueBatterie(puissance_pratique, marge=0.50)`

**Objectif:** Convertir la **puissance pratique batterie en puissance théorique** avec **marge de sécurité**.

**Paramètres:**
- `puissance_pratique`: float (W) - capacité utilisable
- `marge`: float (0-1) - marge de sécurité (0.50 = 50%, configurable)

**Logique (DIFFÉRENT DU PANNEAU):**
```
P_théorique = P_pratique × (1 + Marge)

Cela équivaut à:
P_théorique = P_pratique × (1 + Marge) = P_pratique × 1.50 (pour 50%)
```

**Pourquoi différent du panneau?**
- **Panneau**: Division car perte d'énergie (rendement)
- **Batterie**: Addition car **marge de sécurité** pour durabilité/protection

**Exemple:**
```
- Puissance pratique: 240W
- Marge: 50% (0.50)
- P théorique = 240W × (1 + 0.50) = 240W × 1.50 = 360W

On achète une batterie de 360W qui utilise reellement 240W
```

**Retour:**
```python
{
    'puissance_theorique': float,      # W (à acheter)
    'puissance_pratique': float,       # W (utilisable)
    'marge': float,                    # % marge
    'marge_nominale': float            # W marge
}
```

---

### 10. `dimensionnerSystemeSolaire(consommations, configJournee_matin, configJournee_apres, heureChargeDebut, heureChargeFin, capaciteBatterie, marge_batterie=0.50)`

**Objectif:** FONCTION ORCHESTRATRICE - Dimensionner **complètement le système solaire** (batterie + panneau) en 4 étapes.

**Paramètres:**
- `consommations`: Liste d'objets Consommation
- `configJournee_matin`: ConfigJournee (P1)
- `configJournee_apres`: ConfigJournee (P2)
- `heureChargeDebut`, `heureChargeFin`: str "HH:MM:SS"
- `capaciteBatterie`: float (Wh)
- `marge_batterie`: float (0-1) - marge batterie (défaut 0.50)

**Étapes (utilise les 3 fonctions précédentes):**

```
1. ÉTAPE 1: calculerBesoinsParPeriode()
   → Obtient besoin_matin, besoin_apres, puissance_charge

2. ÉTAPE 2: calculerPuissancePratiquePanneau()
   → Détermine puissance_pratique

3. ÉTAPE 3: calculerPuissanceTheoriquePanneau()
   → Convertit en puissance_theorique (avec rendement)

4. ÉTAPE 4: calculerPuissanceTheoriqueBatterie()
   → Convertit batterie pratique en théorique (avec marge)
```

**Retour:**
```python
{
    'besoins': dict,                       # Détails besoins
    'puissance_pratique': float,           # W panneau utilisable
    'puissance_theorique': float,          # W panneau à acheter
    'batterie_capacite': float,            # Wh capacité
    'batterie_puissance_pratique': float,  # W utilisable
    'batterie_puissance_theorique': float, # W à acheter
    'batterie_marge': float,               # % marge
    'batterie_puissance_charge': float,    # W pour charger
    'rendement_matin': float,              # %
    'logique': str                         # Explication
}
```

---

## ☀️ FONCTIONS CHARGEBATTERIESERVICE

### 1. `calculerPuissanceNecessaire(heureDebut, heureFin, capaciteBatterie)`

**Objectif:** Calculer la **puissance requise pour charger la batterie** dans un intervalle de temps donné.

**Paramètres:**
- `heureDebut`: str "HH:MM:SS" - début de charge
- `heureFin`: str "HH:MM:SS" - fin de charge
- `capaciteBatterie`: float (Wh) - capacité à charger

**Logique:**
1. Calcule la durée en heures (gère traversée minuit)
2. Applique la formule: Puissance = Capacité / Durée

**Formule:**
```
Puissance (W) = Capacité (Wh) / Temps (h)
```

**Retour:**
```python
{
    'puissance_necessaire': float,     # W
    'temps_heures': float,             # h
    'capacite': float,                 # Wh
    'details': dict                    # Détails calcul
}
```

**Exemple:**
```
- Batterie: 240 Wh
- Charge de 10:00 à 14:00 (4h)
- Puissance = 240Wh / 4h = 60W

Pour charger 240Wh en 4 heures, il faut 60W
```

**Cas spéciaux:**
- Gère les charges **dépassant minuit** (ex: 22:00 → 02:00)
- Précision à la **minute**

---

## 📌 RÉSUMÉ DES VARIABLES CLÉS

| Variable | Unité | Signification |
|----------|-------|---------------|
| `puissance` | W | Puissance instantanée d'un appareil |
| `capacite_batterie` | Wh | Énergie totale stockée |
| `energie` | Wh | Puissance × Durée |
| `rendement` | % | Efficacité du panneau (40/80%) |
| `marge` | % | Sécurité batterie (50%) |
| `puissance_pratique` | W | Puissance réelle utilisable |
| `puissance_theorique` | W | Puissance spécifiée/à acheter |

---

## 🔄 FLUX COMPLET DE DIMENSIONNEMENT

```
Consommations + ConfigJournee + Batterie
    ↓
dimensionnerSystemeSolaire()
    ├── calculerBesoinsParPeriode()
    │   ├── calculerPuissancePanneauRequise() [Matin P1]
    │   └── calculerPuissancePanneauRequise() [Après P2]
    │
    ├── calculerPuissancePratiquePanneau()
    │   (Compare besoins matin vs après)
    │
    ├── calculerPuissanceTheoriquePanneau()
    │   (Applique rendement: ÷ 0.40)
    │
    └── calculerPuissanceTheoriqueBatterie()
        (Applique marge: × 1.50)
    ↓
Dimensionnement complet
├── Batterie théorique (W)
└── Panneau théorique (W)
```

---

## 💡 CAS PARTICULIERS GÉRÉS

1. **Appareils traversant minuit** ✓
2. **Appareils traversant plusieurs périodes** ✓
3. **Rendement variable par période** ✓
4. **Marge batterie configurable** ✓
5. **Fenêtre de charge indépendante des périodes** ✓
6. **Précision minute** ✓

