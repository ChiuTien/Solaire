from sqlalchemy import create_engine, text

class Connexion:
    def __init__(self, serve, db, user, password):
        self.serve = serve
        self.db = db

        url = (f'mssql+pyodbc://{user}:{password}@'
                f'{serve}/{db}?driver=ODBC+Driver+17+for+SQL+Server'
                )

        self.engine = create_engine(url)
        self.connection = None
    
    def connect(self):
        try:
            self.connection = self.engine.connect()
            print("Connexion réussie à la base de données.")
        except Exception as e:
            print(f"Erreur de connexion : {e}")

    def execute_query(self, query):
        if self.connection is None:
            print("Aucune connexion établie.")
            return None
        
        try:
            result = self.connection.execute(text(query))
            return result.fetchall()
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return None
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Connexion fermée.")