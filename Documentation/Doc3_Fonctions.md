# DOC 3 - CRÉATION ET APPEL DE FONCTIONS

## Syntaxe de base

Une **fonction** est un bloc de code réutilisable qui effectue une tâche spécifique.

### Fonction simple (sans paramètres)

```python
# Définition
def dire_bonjour():
    """Fonction sans paramètres."""
    print("Bonjour!")

# Appel
dire_bonjour()
```

---

## Fonctions avec paramètres

Les **paramètres** sont des variables que la fonction reçoit.

```python
# Fonction avec paramètres
def additionner(a, b):
    """Additionne deux nombres."""
    return a + b

# Appel
resultat = additionner(5, 3)
print(resultat)  # Affiche: 8
```

---

## Paramètres par défaut

Tu peux donner une **valeur par défaut** à un paramètre.

```python
def saluer(nom, salutation="Bonjour"):
    """Fonction avec paramètre par défaut."""
    print(f"{salutation}, {nom}!")

# Appels
saluer("Alice")  # Utilise le salutation par défaut → "Bonjour, Alice!"
saluer("Bob", "Bonsoir")  # Remplace le paramètre par défaut → "Bonsoir, Bob!"
```

---

## Paramètres nommés

Tu peux nommer les paramètres à l'appel pour plus de clarté.

```python
def creer_profil(nom, email, age, ville="Paris"):
    """Crée un profil utilisateur."""
    return {
        "nom": nom,
        "email": email,
        "age": age,
        "ville": ville
    }

# Appels - version courte (positionnels)
profil1 = creer_profil("Alice", "alice@email.com", 28)

# Appels - version longue (nommés)
profil2 = creer_profil(
    nom="Bob",
    email="bob@email.com",
    age=35,
    ville="Lyon"
)

print(profil1)
# {'nom': 'Alice', 'email': 'alice@email.com', 'age': 28, 'ville': 'Paris'}

print(profil2)
# {'nom': 'Bob', 'email': 'bob@email.com', 'age': 35, 'ville': 'Lyon'}
```

---

## Fonctions avec *args (nombre variable d'arguments)

La syntaxe `*args` permet d'accepter un **nombre variable d'arguments**.

```python
# *args: nombre variable d'arguments (tuple)
def afficher_nombres(*nombres):
    """Affiche tous les nombres passés."""
    for nombre in nombres:
        print(nombre)

# Appels avec différents nombres d'arguments
afficher_nombres(1)
afficher_nombres(1, 2)
afficher_nombres(1, 2, 3, 4, 5)
```

**Exemple utile:**

```python
def somme(*nombres):
    """Calcule la somme de tous les nombres."""
    total = 0
    for nombre in nombres:
        total += nombre
    return total

print(somme(1, 2, 3))        # 6
print(somme(10, 20, 30, 40))  # 100
```

---

## Fonctions avec **kwargs (arguments nommés variables)

La syntaxe `**kwargs` permet d'accepter des **arguments nommés variables** (dictionnaire).

```python
# **kwargs: arguments nommés variables (dictionnaire)
def afficher_donnees(**donnees):
    """Affiche toutes les données."""
    for cle, valeur in donnees.items():
        print(f"{cle}: {valeur}")

# Appel
afficher_donnees(nom="Alice", age=28, ville="Paris")
# Affiche:
# nom: Alice
# age: 28
# ville: Paris
```

**Exemple utile:**

```python
def creer_utilisateur(**kwargs):
    """Crée un utilisateur avec les informations fournies."""
    utilisateur = {}
    for cle, valeur in kwargs.items():
        utilisateur[cle] = valeur
    return utilisateur

user = creer_utilisateur(nom="Alice", email="alice@email.com", age=28)
print(user)
# {'nom': 'Alice', 'email': 'alice@email.com', 'age': 28}
```

---

## Combiner tous les types

```python
def fonction_complete(a, b, c=10, *args, **kwargs):
    """Fonction combinant tous les types de paramètres."""
    print(f"a={a}, b={b}, c={c}")
    print(f"args={args}")
    print(f"kwargs={kwargs}")

# Appel
fonction_complete(1, 2, 3, 4, 5, nom="Alice", age=28)
# a=1, b=2, c=3
# args=(4, 5)
# kwargs={'nom': 'Alice', 'age': 28}
```

---

## Exemple complet: Fonctions utiles

```python
def valider_email(email):
    """Valide un email."""
    return "@" in email and "." in email

def calculer_remise(prix, pourcentage):
    """Calcule le prix avec remise."""
    return prix * (1 - pourcentage / 100)

def obtenir_info_utilisateur(nom, email, age):
    """Récupère les infos d'un utilisateur."""
    if not valider_email(email):
        return "Email invalide!"
    
    return {
        "nom": nom,
        "email": email,
        "adulte": age >= 18
    }

# Utilisation
print(valider_email("alice@email.com"))  # True
print(valider_email("alice_email.com"))  # False

print(calculer_remise(100, 20))  # 80.0 (20% de remise)
print(calculer_remise(50, 10))   # 45.0 (10% de remise)

print(obtenir_info_utilisateur("Alice", "alice@email.com", 28))
# {'nom': 'Alice', 'email': 'alice@email.com', 'adulte': True}

print(obtenir_info_utilisateur("Bob", "bob_email.com", 17))
# Email invalide!
```

---

## Points clés à retenir:

✓ **À faire:**
- Donner des noms clairs aux fonctions
- Documenter chaque fonction avec une docstring
- Retourner des valeurs inappropriées
- Utiliser des paramètres par défaut pour les options

✗ **À éviter:**
- Fonctions trop longues (max 50 lignes)
- Trop de paramètres (max 5)
- Pas de documentation
- Effets de bord non explicites

---

## Différents types de retour:

```python
# 1. Sans retour (retourne None)
def afficher(message):
    print(message)

# 2. Avec retour simple
def additionner(a, b):
    return a + b

# 3. Avec retour multiple (tuple)
def diviser(a, b):
    quotient = a // b
    reste = a % b
    return quotient, reste

q, r = diviser(10, 3)
print(q, r)  # 3 1

# 4. Avec retour conditionnel
def max_de_deux(a, b):
    if a > b:
        return a
    else:
        return b
```

---

## Résumé des paramètres:

| Type | Syntaxe | Exemple |
|------|---------|---------|
| Normal | `def f(a, b)` | `f(1, 2)` |
| Par défaut | `def f(a, b=10)` | `f(1)` ou `f(1, 20)` |
| Nommé | `def f(a, b)` | `f(a=1, b=2)` |
| Variable | `def f(*args)` | `f(1, 2, 3, 4)` |
| Nommé variable | `def f(**kwargs)` | `f(a=1, b=2, c=3)` |

Bonne chance! 🚀
