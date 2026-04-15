from Database.Connexion import Connexion

# 1. Créer une instance avec tes paramètres
connexion = Connexion(
    serve="127.0.0.1,1433",      # ← Ton serveur Docker
    db="Solaris",                  # ← Le nom de ta DB
    user="sa",                     # ← L'utilisateur SQL Server
    password="MotDePasseFort123!"    # ← Le mot de passe
)

# 2. Se connecter
connexion.connect()

# 3. Tester une requête simple
resultat = connexion.execute_query("SELECT @@VERSION")
if resultat:
    print(f"Version SQL Server: {resultat[0]}")

# 4. Se déconnecter
connexion.disconnect()