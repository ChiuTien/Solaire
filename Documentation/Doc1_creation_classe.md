# DOC 1 - CRÉATION DE CLASSE AVEC ENCAPSULATION

## Concept clé
L'**encapsulation** est un concept fondamental de la programmation orientée objet. Elle permet de **protéger** les attributs d'une classe en les rendant "privés" et d'y accéder uniquement via des **getters** et **setters**.

### En Python:
- Attribut privé: `_attribut` (conventionnel, Python ne l'empêche pas vraiment)
- Attribut très privé: `__attribut` (name mangling - plus difficile d'y accéder)

---

## Exemple 1: Classe avec Getters et Setters classiques

```python
class Utilisateur:
    """Classe représentant un utilisateur avec attributs encapsulés."""
    
    def __init__(self, nom, email, age):
        """Constructeur - initialise les attributs privés."""
        self.__nom = nom
        self.__email = email
        self.__age = age
    
    # ========== GETTERS ==========
    # Permettent de LIRE les valeurs privées
    
    def get_nom(self):
        """Retourne le nom de l'utilisateur."""
        return self.__nom
    
    def get_email(self):
        """Retourne l'email de l'utilisateur."""
        return self.__email
    
    def get_age(self):
        """Retourne l'âge de l'utilisateur."""
        return self.__age
    
    # ========== SETTERS ==========
    # Permettent de MODIFIER les valeurs privées avec validations
    
    def set_nom(self, nom):
        """Modifie le nom avec validation."""
        if isinstance(nom, str) and len(nom) > 0:
            self.__nom = nom
        else:
            print("Erreur: Le nom doit être une chaîne non vide")
    
    def set_email(self, email):
        """Modifie l'email avec validation."""
        if "@" in email and "." in email:
            self.__email = email
        else:
            print("Erreur: Email invalide")
    
    def set_age(self, age):
        """Modifie l'âge avec validation."""
        if isinstance(age, int) and 0 <= age <= 150:
            self.__age = age
        else:
            print("Erreur: L'âge doit être entre 0 et 150")
    
    def afficher_info(self):
        """Affiche les informations de l'utilisateur."""
        return f"Nom: {self.__nom}, Email: {self.__email}, Âge: {self.__age}"
```

### Utilisation:

```python
# Créer un utilisateur
user = Utilisateur("Alice Dupont", "alice@email.com", 28)

# Lire les valeurs avec getters
print(f"Nom: {user.get_nom()}")
print(f"Email: {user.get_email()}")
print(f"Âge: {user.get_age()}")

# Modifier les valeurs avec setters
user.set_age(29)
user.set_email("alice.dupont@newmail.com")
print(user.afficher_info())

# Essayer une modification invalide (sera rejetée)
user.set_age(200)  # Affiche une erreur
```

---

## Exemple 2: Classe avec Décorateurs @property (méthode moderne)

```python
class Produit:
    """Exemple avec décorateurs @property - approche plus Pythonic."""
    
    def __init__(self, nom, prix):
        self.__nom = nom
        self.__prix = prix
    
    # Décorateur @property pour créer un getter
    @property
    def nom(self):
        """Getter pour le nom."""
        return self.__nom
    
    # Décorateur @nom.setter pour créer un setter
    @nom.setter
    def nom(self, valeur):
        """Setter pour le nom."""
        if isinstance(valeur, str) and len(valeur) > 0:
            self.__nom = valeur
    
    @property
    def prix(self):
        """Getter pour le prix."""
        return self.__prix
    
    @prix.setter
    def prix(self, valeur):
        """Setter pour le prix."""
        if isinstance(valeur, (int, float)) and valeur >= 0:
            self.__prix = valeur
        else:
            print("Erreur: Prix doit être positif")
```

### Utilisation avec @property:

```python
# Créer un produit
produit = Produit("Laptop", 999.99)

# Utiliser comme des attributs normaux
print(f"Produit: {produit.nom}, Prix: {produit.prix}€")

# Modifier avec le setter
produit.prix = 899.99
print(f"Nouveau prix: {produit.prix}€")

# Essayer une modification invalide
produit.prix = -100  # Sera rejeté
```

---

## Points clés à retenir:

✓ **À faire:**
- Toujours utiliser des attributs privés (`__attribut`)
- Créer des getters pour lire les valeurs
- Créer des setters pour modifier les valeurs
- Ajouter des validations dans les setters
- Documenter chaque getter et setter

✗ **À éviter:**
- Accéder directement aux attributs privés
- Faire des modifications sans validation
- Oublier de documenter le code

---

## Différence entre approches:

| Aspect | Getters/Setters classiques | @property |
|--------|---------------------------|-----------|
| **Syntaxe** | `obj.get_nom()` | `obj.nom` |
| **Lisibilité** | Verbose | Plus claire |
| **Performance** | Léger surcoût | Minime |
| **Recommandé** | Pour les debutants | Pour la production |

Bonne chance! 🚀
