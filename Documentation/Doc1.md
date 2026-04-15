# LEÇONS PYTHON - GUIDE COMPLET

## TABLE DES MATIÈRES
1. [Leçon 1: Création de classe avec encapsulation](#leçon-1)
2. [Leçon 2: Connexion avec SQL Server](#leçon-2)
3. [Leçon 3: Création et appel de fonctions](#leçon-3)
4. [Leçon 4: Opérations CRUD](#leçon-4)

---

## LEÇON 1: CRÉATION DE CLASSE AVEC ENCAPSULATION {#leçon-1}

### Concept clé
L'**encapsulation** est un concept fondamental de la programmation orientée objet. Elle permet de **protéger** les attributs d'une classe en les rendant "privés" et d'y accéder uniquement via des **getters** et **setters**.

### En Python:
- Attribut privé: `_attribut` (conventionnel, Python ne l'empêche pas vraiment)
- Attribut très privé: `__attribut` (name mangling - plus difficile d'y accéder)

---

### Exemple 1: Classe avec Getters et Setters classiques

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

### Exemple 2: Classe avec Décorateurs @property (méthode moderne)

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

## LEÇON 2: CONNEXION AVEC SQL SERVER {#leçon-2}

### Installation du driver SQL Server

```bash
pip install pyodbc
```

ou avec SQLAlchemy (recommandé):

```bash
pip install sqlalchemy
```

---

### Exemple 1: Connexion simple avec pyodbc

```python
import pyodbc

class ConnexionBD:
    """Classe pour gérer la connexion à SQL Server."""
    
    def __init__(self, serveur, base_de_donnees, utilisateur, motdepasse):
        """
        Initialise la connexion.
        
        Args:
            serveur (str): Nom du serveur SQL Server
            base_de_donnees (str): Nom de la base de données
            utilisateur (str): Nom d'utilisateur
            motdepasse (str): Mot de passe
        """
        self.serveur = serveur
        self.base_de_donnees = base_de_donnees
        self.utilisateur = utilisateur
        self.motdepasse = motdepasse
        self.connexion = None
    
    def se_connecter(self):
        """Établit la connexion à la bases de données."""
        try:
            # Chaîne de connexion
            chaine_connexion = (
                f'Driver={{ODBC Driver 17 for SQL Server}};'
                f'Server={self.serveur};'
                f'Database={self.base_de_donnees};'
                f'UID={self.utilisateur};'
                f'PWD={self.motdepasse}'
            )
            
            self.connexion = pyodbc.connect(chaine_connexion)
            print("✓ Connexion établie avec succès!")
            return True
        
        except pyodbc.Error as e:
            print(f"✗ Erreur de connexion: {e}")
            return False
    
    def se_deconnecter(self):
        """Ferme la connexion."""
        if self.connexion:
            self.connexion.close()
            print("✓ Connexion fermée")
    
    def executer_requete(self, requete):
        """
        Exécute une requête SQL.
        
        Args:
            requete (str): Requête SQL à exécuter
        
        Returns:
            Cursor: Objet cursor pour accéder aux résultats
        """
        try:
            cursor = self.connexion.cursor()
            cursor.execute(requete)
            self.connexion.commit()
            return cursor
        except Exception as e:
            print(f"Erreur lors de l'exécution: {e}")
            return None
```

### Utilisation:

```python
# Créer et établir une connexion
bd = ConnexionBD(
    serveur='LAPTOP-ABC\\SQLEXPRESS',  # Ou nom du serveur
    base_de_donnees='MaBaseDeDonnees',
    utilisateur='utilisateur',
    motdepasse='monmotdepasse'
)

# Se connecter
if bd.se_connecter():
    # Exécuter une requête
    curseur = bd.executer_requete("SELECT * FROM Utilisateurs")
    
    # Parcourir les résultats
    for ligne in curseur.fetchall():
        print(ligne)
    
    # Se déconnecter
    bd.se_deconnecter()
```

---

### Exemple 2: Connexion avec SQLAlchemy (recommandée)

```python
from sqlalchemy import create_engine, text

class ConnexionBDAlchemy:
    """Classe pour gérer SQL Server avec SQLAlchemy."""
    
    def __init__(self, serveur, base_donnees, utilisateur, motdepasse):
        self.serveur = serveur
        self.base_donnees = base_donnees
        
        # Créer l'URL de connexion
        url = (
            f'mssql+pyodbc://{utilisateur}:{motdepasse}@'
            f'{serveur}/{base_donnees}?driver=ODBC+Driver+17+for+SQL+Server'
        )
        
        self.engine = create_engine(url)
        self.connexion = None
    
    def se_connecter(self):
        """Établit la connexion."""
        try:
            self.connexion = self.engine.connect()
            print("✓ Connexion SQLAlchemy établie!")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def executer_requete(self, requete):
        """Exécute une requête SQL."""
        try:
            resultat = self.connexion.execute(text(requete))
            return resultat.fetchall()
        except Exception as e:
            print(f"Erreur: {e}")
            return None
    
    def se_deconnecter(self):
        """Ferme la connexion."""
        if self.connexion:
            self.connexion.close()
```

---

## LEÇON 3: CRÉATION ET APPEL DE FONCTIONS {#leçon-3}

### Syntaxe de base

```python
# Fonction simple
def dire_bonjour():
    """Fonction sans paramètres."""
    print("Bonjour!")

# Appel
dire_bonjour()
```

---

### Fonctions avec paramètres

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

### Paramètres par défaut

```python
def saluer(nom, salutation="Bonjour"):
    """Fonction avec paramètre par défaut."""
    print(f"{salutation}, {nom}!")

# Appels
saluer("Alice")  # Utilise le salutation par défaut
saluer("Bob", "Bonsoir")  # Remplace le paramètre par défaut
```

---

### Paramètres nommés

```python
def creer_profil(nom, email, age, ville="Paris"):
    """Crée un profil utilisateur."""
    return {
        "nom": nom,
        "email": email,
        "age": age,
        "ville": ville
    }

# Appels
profil1 = creer_profil("Alice", "alice@email.com", 28)
profil2 = creer_profil(
    nom="Bob",
    email="bob@email.com",
    age=35,
    ville="Lyon"
)

print(profil1)
print(profil2)
```

---

### Fonctions avec *args et **kwargs

```python
# *args: nombre variable d'arguments (tuple)
def afficher_nombres(*nombres):
    """Affiche tous les nombres passés."""
    for nombre in nombres:
        print(nombre)

afficher_nombres(1, 2, 3, 4, 5)

# **kwargs: arguments nommés variables (dictionnaire)
def afficher_donnees(**donnees):
    """Affiche toutes les données."""
    for cle, valeur in donnees.items():
        print(f"{cle}: {valeur}")

afficher_donnees(nom="Alice", age=28, ville="Paris")
```

---

### Exemple complet: Fonctions utiles

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
print(calculer_remise(100, 20))  # 80
print(obtenir_info_utilisateur("Alice", "alice@email.com", 28))
```

---

## LEÇON 4: OPÉRATIONS CRUD {#leçon-4}

### Qu'est-ce que CRUD?
- **C**reate: Créer (INSERT)
- **R**ead: Lire (SELECT)
- **U**pdate: Mettre à jour (UPDATE)
- **D**elete: Supprimer (DELETE)

---

### Structure de la table exemple

```sql
CREATE TABLE Utilisateurs (
    id INT PRIMARY KEY IDENTITY(1,1),
    nom NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    age INT,
    ville NVARCHAR(100)
)
```

---

### Classe CRUD complète

```python
import pyodbc
from datetime import datetime

class CRUDUtilisateur:
    """Classe pour gérer les opérations CRUD sur les utilisateurs."""
    
    def __init__(self, connexion):
        """
        Initialise le gestionnaire CRUD.
        
        Args:
            connexion: Objet connexion déjà établi
        """
        self.connexion = connexion
    
    # ========== CREATE ==========
    def creer_utilisateur(self, nom, email, age, ville):
        """
        Crée un nouvel utilisateur.
        
        Args:
            nom (str): Nom de l'utilisateur
            email (str): Email
            age (int): Âge
            ville (str): Ville
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            cursor = self.connexion.cursor()
            requete = """
                INSERT INTO Utilisateurs (nom, email, age, ville)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(requete, (nom, email, age, ville))
            self.connexion.commit()
            print(f"✓ Utilisateur '{nom}' créé avec succès")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de la création: {e}")
            return False
    
    # ========== READ ==========
    def lire_tous_utilisateurs(self):
        """
        Récupère tous les utilisateurs.
        
        Returns:
            list: Liste de tuples contenant les données
        """
        try:
            cursor = self.connexion.cursor()
            requete = "SELECT id, nom, email, age, ville FROM Utilisateurs"
            cursor.execute(requete)
            return cursor.fetchall()
        except Exception as e:
            print(f"✗ Erreur lors de la lecture: {e}")
            return None
    
    def lire_utilisateur_par_id(self, id_utilisateur):
        """
        Récupère un utilisateur par son ID.
        
        Args:
            id_utilisateur (int): L'ID de l'utilisateur
        
        Returns:
            tuple: Les données de l'utilisateur
        """
        try:
            cursor = self.connexion.cursor()
            requete = "SELECT * FROM Utilisateurs WHERE id = ?"
            cursor.execute(requete, (id_utilisateur,))
            return cursor.fetchone()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def lire_utilisateur_par_email(self, email):
        """
        Récupère un utilisateur par son email.
        
        Args:
            email (str): L'email
        
        Returns:
            tuple: Les données de l'utilisateur
        """
        try:
            cursor = self.connexion.cursor()
            requete = "SELECT * FROM Utilisateurs WHERE email = ?"
            cursor.execute(requete, (email,))
            return cursor.fetchone()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    # ========== UPDATE ==========
    def modifier_utilisateur(self, id_utilisateur, nom=None, email=None, age=None, ville=None):
        """
        Modifie un utilisateur (met à jour les champs fournis).
        
        Args:
            id_utilisateur (int): L'ID de l'utilisateur
            nom, email, age, ville: Les champs à modifier (None = ne pas modifier)
        
        Returns:
            bool: True si succès
        """
        try:
            cursor = self.connexion.cursor()
            
            # Récupérer l'utilisateur actuel
            utilisateur = self.lire_utilisateur_par_id(id_utilisateur)
            if not utilisateur:
                print(f"✗ Utilisateur {id_utilisateur} non trouvé")
                return False
            
            # Garder les valeurs actuelles pour les champs non spécifiés
            nouveau_nom = nom or utilisateur[1]
            nouveau_email = email or utilisateur[2]
            nouvel_age = age or utilisateur[3]
            nouvelle_ville = ville or utilisateur[4]
            
            # Exécuter la mise à jour
            requete = """
                UPDATE Utilisateurs
                SET nom = ?, email = ?, age = ?, ville = ?
                WHERE id = ?
            """
            cursor.execute(requete, (nouveau_nom, nouveau_email, nouvel_age, nouvelle_ville, id_utilisateur))
            self.connexion.commit()
            print(f"✓ Utilisateur {id_utilisateur} modifié")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de la modification: {e}")
            return False
    
    # ========== DELETE ==========
    def supprimer_utilisateur(self, id_utilisateur):
        """
        Supprime un utilisateur.
        
        Args:
            id_utilisateur (int): L'ID de l'utilisateur
        
        Returns:
            bool: True si succès
        """
        try:
            cursor = self.connexion.cursor()
            requete = "DELETE FROM Utilisateurs WHERE id = ?"
            cursor.execute(requete, (id_utilisateur,))
            self.connexion.commit()
            print(f"✓ Utilisateur {id_utilisateur} supprimé")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de la suppression: {e}")
            return False
    
    # ========== BONUS: Méthodes utiles ==========
    def compter_utilisateurs(self):
        """Compte le nombre d'utilisateurs."""
        try:
            cursor = self.connexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM Utilisateurs")
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return 0
    
    def obtenir_utilisateurs_par_ville(self, ville):
        """Récupère tous les utilisateurs d'une ville."""
        try:
            cursor = self.connexion.cursor()
            requete = "SELECT * FROM Utilisateurs WHERE ville = ?"
            cursor.execute(requete, (ville,))
            return cursor.fetchall()
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
```

---

### Exemple d'utilisation complet

```python
# Supposons que la connexion est déjà établie
connexion = creer_connexion()  # Fonction définie précédemment

# Créer un gestionnaire CRUD
crud = CRUDUtilisateur(connexion)

# ===== CRÉER =====
print("\n=== CRÉATION ===")
crud.creer_utilisateur("Alice Dupont", "alice@email.com", 28, "Paris")
crud.creer_utilisateur("Bob Martin", "bob@email.com", 35, "Lyon")
crud.creer_utilisateur("Carol Johnson", "carol@email.com", 32, "Paris")

# ===== LIRE =====
print("\n=== LECTURE ===")

# Tous les utilisateurs
print("\nTous les utilisateurs:")
utilisateurs = crud.lire_tous_utilisateurs()
for user in utilisateurs:
    print(f"  {user}")

# Rechercher par ID
print("\nUtilisateur avec ID 1:")
user = crud.lire_utilisateur_par_id(1)
print(f"  {user}")

# Rechercher par email
print("\nUtilisateur avec email 'bob@email.com':")
user = crud.lire_utilisateur_par_email("bob@email.com")
print(f"  {user}")

# Utilisateurs d'une ville
print("\nUtilisateurs de Paris:")
parisiens = crud.obtenir_utilisateurs_par_ville("Paris")
for user in parisiens:
    print(f"  {user}")

# ===== MODIFIER =====
print("\n=== MODIFICATION ===")
crud.modifier_utilisateur(1, age=29)  # Modifier seulement l'âge
crud.modifier_utilisateur(2, ville="Marseille")  # Changer la ville

# Vérifier la modification
print("\nAprès modification (ID 2):")
user = crud.lire_utilisateur_par_id(2)
print(f"  {user}")

# ===== SUPPRIMER =====
print("\n=== SUPPRESSION ===")
crud.supprimer_utilisateur(3)

# Vérifier la suppression
print(f"\nNombre d'utilisateurs restants: {crud.compter_utilisateurs()}")

# Se déconnecter
connexion.close()
```

---

### Résultat attendu

```
=== CRÉATION ===
✓ Utilisateur 'Alice Dupont' créé avec succès
✓ Utilisateur 'Bob Martin' créé avec succès
✓ Utilisateur 'Carol Johnson' créé avec succès

=== LECTURE ===

Tous les utilisateurs:
  (1, 'Alice Dupont', 'alice@email.com', 28, 'Paris')
  (2, 'Bob Martin', 'bob@email.com', 35, 'Lyon')
  (3, 'Carol Johnson', 'carol@email.com', 32, 'Paris')

Utilisateur avec ID 1:
  (1, 'Alice Dupont', 'alice@email.com', 28, 'Paris')

... (résultats des autres lectures)

=== MODIFICATION ===
✓ Utilisateur 1 modifié
✓ Utilisateur 2 modifié

=== SUPPRESSION ===
✓ Utilisateur 3 supprimé

Nombre d'utilisateurs restants: 2
```

---

### Bonnes pratiques CRUD

✓ **À faire:**
- Valider les données avant de les insérer
- Utiliser des requêtes paramétrées pour la sécurité
- Gérer les erreurs avec try/except
- Fermer les connexions
- Documenter chaque opération

✗ **À éviter:**
- Concaténer les variables dans les requêtes SQL (failles de sécurité)
- Ignorer les erreurs
- Oublier de valider les entrées utilisateur
- Faire des requêtes trop complexes

---

## RÉSUMÉ

| Concept | Utilité |
|---------|---------|
| **Encapsulation** | Protéger les données avec getters/setters |
| **Connexion BD** | Établir une communication avec SQL Server |
| **Fonctions** | Réutiliser du code et organiser le programme |
| **CRUD** | Gérer complètement les données en base |

Bonne chance! 🚀
