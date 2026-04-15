# DOC 2 - CONNEXION AVEC BASE DE DONNÉES SQL SERVER

## Qu'est-ce qu'un serveur SQL Server?

**SQL Server** est un **système de gestion de base de données** (SGBD) développé par Microsoft. Pour vous connecter à une base de données, vous devez connaître:

1. **Le serveur** - L'ordinateur où se trouve SQL Server (l'adresse IP ou le nom)
2. **La base de données** - Le nom de la BD que vous voulez utiliser
3. **Les identifiants** - Nom d'utilisateur et mot de passe pour accéder au serveur

---

## Comment identifier votre serveur SQL Server?

#### Si vous avez SQL Server installé localement:

**Sur Windows:**
- Ouvrez **SQL Server Management Studio (SSMS)**
- Regardez le nom du serveur dans l'explorateur d'objets (en haut à gauche)
- Il ressemble généralement à: `LAPTOP-XXXXX\SQLEXPRESS` ou `.\SQLEXPRESS`

```
Exemples courants:
- (local)              = Serveur local
- .\SQLEXPRESS        = Serveur local avec instance SQLEXPRESS
- LAPTOP-ABC\SQLEXPRESS = Ordinateur "LAPTOP-ABC", instance "SQLEXPRESS"
- 192.168.1.100       = Adresse IP du serveur
- serveur.company.com = Serveur distant
```

---

## Composants de la chaîne de connexion

```
Driver={ODBC Driver 17 for SQL Server};
Server=LAPTOP-ABC\SQLEXPRESS;
Database=MaBaseDeDonnees;
UID=utilisateur;
PWD=motdepasse
```

**Explication:**
- `Driver`: Le pilote ODBC à utiliser (17 = version récente)
- `Server`: **Le serveur SQL Server** (ce que vous cherchez!)
- `Database`: Le nom de la base de données
- `UID`: Votre nom d'utilisateur (par défaut: `sa` ou votre user Windows)
- `PWD`: Votre mot de passe

---

## Les différents types de serveurs

#### 1️⃣ **Serveur local avec authentification Windows**

```python
# Utilise votre compte Windows pour vous connecter
chaine_connexion = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=LAPTOP-ABC\\SQLEXPRESS;'
    'Database=MaBaseDeDonnees;'
    'Trusted_Connection=yes;'  # Utilise l'authentification Windows
)

connexion = pyodbc.connect(chaine_connexion)
```

#### 2️⃣ **Serveur local avec authentification SQL Server**

```python
# Utilise un utilisateur SQL Server (par défaut: 'sa')
chaine_connexion = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=.\\SQLEXPRESS;'
    'Database=MaBaseDeDonnees;'
    'UID=sa;'
    'PWD=MonMotDePasse123;'
)

connexion = pyodbc.connect(chaine_connexion)
```

#### 3️⃣ **Serveur distant (en ligne)**

```python
# Connexion à un serveur sur le réseau ou sur Azure
chaine_connexion = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=serveur.database.windows.net;'  # URL du serveur
    'Database=MaBaseDeDonnees;'
    'UID=utilisateur@serveur;'
    'PWD=MotDePasseSecurise;'
)

connexion = pyodbc.connect(chaine_connexion)
```

---

## Installation du driver SQL Server et ODBC

### **Étape 1: Installer les paquets Python**

```bash
# Installer pyodbc
pip install pyodbc

# Installer SQLAlchemy (optionnel mais recommandé)
pip install sqlalchemy
```

---

### **Étape 2: Installer le driver ODBC Microsoft**

**⚠️ IMPORTANT:** Sans cette étape, tu auras l'erreur: `Can't open lib 'ODBC Driver 17 for SQL Server'`

#### 📦 **Sur Ubuntu/Debian:**

```bash
# 1. Ajouter la clé Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -

# 2. Ajouter le dépôt Microsoft
sudo add-apt-repository "$(curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list)"

# 3. Mettre à jour les paquets
sudo apt-get update

# 4. Installer le driver ODBC
sudo apt-get install -y msodbcsql17

# 5. Installer les outils optionnels (sqlcmd, bcp)
sudo apt-get install -y mssql-tools17
```

---

#### 🐧 **Sur CachyOS (Arch-based):**

```bash
# 1. Installer depuis AUR avec yay (si tu l'as)
yay -S msodbcsql

# OU manuellement avec makepkg:

# 1. Cloner le dépôt AUR
git clone https://aur.archlinux.org/msodbcsql.git
cd msodbcsql

# 2. Installer les dépendances
sudo pacman -S base-devel unixodbc

# 3. Compiler et installer
makepkg -sri

# OU utiliser pamac (si tu as Pamac)
pamac install msodbcsql
```

---

#### **Autres distributions Linux:**

**Fedora/RHEL/CentOS:**
```bash
sudo yum install -y msodbcsql17
```

**Alpine:**
```bash
apk add msodbc
```

---

### **Étape 3: Vérifier l'installation**

```bash
# Vérifier que le driver ODBC est bien installé
odbcinst -j

# Tu devras voir quelque chose comme:
# DRIVERS............: /etc/odbcinst.ini
# SYSTEM DATA SOURCES: /etc/odbc.ini
# FILE DATA SOURCES..: /etc/ODBCDataSources
# USER DATA SOURCES..: /home/utilisateur/.odbc.ini
# SQLUSERINI.........: /home/utilisateur/.sqlrc
```

---

## Résumé des installations requises:

| Composant | Installation | Commande |
|-----------|-------------|----------|
| **pyodbc** | Python | `pip install pyodbc` |
| **SQLAlchemy** | Python (optionnel) | `pip install sqlalchemy` |
| **Driver ODBC 17** | Système (Ubuntu) | `sudo apt-get install msodbcsql17` |
| **Driver ODBC 17** | Système (CachyOS) | `yay -S msodbcsql` ou `pamac install msodbcsql` |

⚠️ **Tu dois installer TOUS les composants pour que ça marche!**

---

## Exemple 1: Connexion simple avec pyodbc

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
    serveur='127.0.0.1,1433',      # Serveur (Docker par exemple)
    base_de_donnees='MaBaseDeDonnees',
    utilisateur='sa',
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

## Exemple 2: Connexion avec SQLAlchemy (recommandée)

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

## Résolution des problèmes

#### ❌ Erreur: "Login failed for user 'sa'"

```
Solution: Vérifiez le mot de passe
- Assurez-vous que le mot de passe est correct
- Vérifiez si SQL Server utilise l'authentification SQL (pas Windows)
```

#### ❌ Erreur: "Named Pipes Provider, error: 40"

```
Solution: Le serveur n'existe pas ou n'est pas accessible
- Vérifiez le nom du serveur
- Assurez-vous que SQL Server est en marche
- Vérifiez le pare-feu
```

#### ❌ Erreur: "Can't open lib 'ODBC Driver 17 for SQL Server'"

```
Solution: Installer le driver ODBC (voir Étape 2 ci-dessus)
```

---

## Tester rapidement votre connexion

```python
import pyodbc

# Configuration
SERVEUR = "127.0.0.1,1433"          # À adapter
BASE = "MaBaseDeDonnees"            # À adapter
USER = "sa"                         # À adapter
PWD = "motdepasse"                  # À adapter

def tester_connexion():
    """Teste rapidement la connexion au serveur."""
    try:
        chaine = (
            f'Driver={{ODBC Driver 17 for SQL Server}};'
            f'Server={SERVEUR};'
            f'Database={BASE};'
            f'UID={USER};'
            f'PWD={PWD}'
        )
        
        conn = pyodbc.connect(chaine)
        cursor = conn.cursor()
        
        # Tester une requête simple
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()
        print(f"✓ Connexion réussie!")
        print(f"✓ Version SQL Server: {version[0]}")
        
        conn.close()
        return True
    
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False

# Exécuter le test
if tester_connexion():
    print("\n✓ Vous pouvez commencer à utiliser la connexion!")
else:
    print("\n✗ Vérifiez vos paramètres de connexion")
```

Bonne chance! 🚀
