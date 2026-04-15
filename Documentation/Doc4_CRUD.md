# DOC 4 - OPÉRATIONS CRUD

## Qu'est-ce que CRUD?

**CRUD** est l'acronyme pour les 4 opérations fondamentales sur une base de données:

- **C** - Create: Créer (INSERT)
- **R** - Read: Lire (SELECT)
- **U** - Update: Mettre à jour (UPDATE)
- **D** - Delete: Supprimer (DELETE)

---

## Structure de la table exemple

Avant de pouvoir utiliser CRUD, tu dois créer une table:

```sql
CREATE TABLE Utilisateurs (
    id INT PRIMARY KEY IDENTITY(1,1),
    nom NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    age INT,
    ville NVARCHAR(100)
)
```

**Explication:**
- `id`: Identifiant unique (auto-incrémenté)
- `nom`: Nom de l'utilisateur (obligatoire)
- `email`: Email (obligatoire)
- `age`: Age (optionnel)
- `ville`: Ville de résidence (optionnelle)

---

## Classe CRUD complète

```python
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

## Exemple d'utilisation complet

```python
# Supposons que la connexion est déjà établie
from Database.Connexion import Connexion

# Créer et établir la connexion
connexion = Connexion(
    serve="127.0.0.1,1433",
    db="MaBaseDeDonnees",
    user="sa",
    password="monmotdepasse"
)
connexion.connect()

# Créer un gestionnaire CRUD
crud = CRUDUtilisateur(connexion.connection)

# ===== CREATE =====
print("\n=== CRÉATION ===")
crud.creer_utilisateur("Alice Dupont", "alice@email.com", 28, "Paris")
crud.creer_utilisateur("Bob Martin", "bob@email.com", 35, "Lyon")
crud.creer_utilisateur("Carol Johnson", "carol@email.com", 32, "Paris")

# ===== READ =====
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

# ===== UPDATE =====
print("\n=== MODIFICATION ===")
crud.modifier_utilisateur(1, age=29)  # Modifier seulement l'âge
crud.modifier_utilisateur(2, ville="Marseille")  # Changer la ville

# Vérifier la modification
print("\nAprès modification (ID 2):")
user = crud.lire_utilisateur_par_id(2)
print(f"  {user}")

# ===== DELETE =====
print("\n=== SUPPRESSION ===")
crud.supprimer_utilisateur(3)

# Vérifier la suppression
print(f"\nNombre d'utilisateurs restants: {crud.compter_utilisateurs()}")

# Se déconnecter
connexion.disconnect()
```

---

## Résultat attendu

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

## Bonnes pratiques CRUD

✓ **À faire:**
- Valider les données avant de les insérer
- Utiliser des requêtes paramétrées pour la sécurité (avec `?`)
- Gérer les erreurs avec try/except
- Fermer les connexions après utilisation
- Documenter chaque opération
- Utiliser des transactions (commit/rollback)

✗ **À éviter:**
- Concaténer les variables dans les requêtes SQL (failles de sécurité)
  - ❌ `f"SELECT * FROM Utilisateurs WHERE id = {id}"`
  - ✅ `"SELECT * FROM Utilisateurs WHERE id = ?" avec cursor.execute(requete, (id,))`
- Ignorer les erreurs
- Oublier de valider les entrées utilisateur
- Faire des requêtes trop complexes sans commentaires
- Modifier les données sans vérifier

---

## Résumé des opérations:

| Opération | SQL | Fonction | Utilité |
|-----------|-----|----------|---------|
| **CREATE** | INSERT | `creer_utilisateur()` | Ajouter une nouvelle ligne |
| **READ** | SELECT | `lire_tous_utilisateurs()` | Récupérer les données |
| **UPDATE** | UPDATE | `modifier_utilisateur()` | Modifier une ligne existante |
| **DELETE** | DELETE | `supprimer_utilisateur()` | Supprimer une ligne |

Bonne chance! 🚀
