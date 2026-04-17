import tkinter as tk
from tkinter import ttk, messagebox
from datetime import time, datetime
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from Models.Consommation import Consommation
from Models.Materiel import Materiel
from Models.ConfigJournee import ConfigJournee
from Models.ChargeBatterie import ChargeBatterie
from Services.ConsommationService import ConsommationService
from Database.Connexion import Connexion
from Repositories.ConsommationRepository import ConsommationRepository
from Repositories.MaterielRepository import MaterielRepository


class DatabaseConfig:
    """Configuration de la base de données."""
    def __init__(self):
        self.serveur = "127.0.0.1,1433"
        self.db = "Solaris"
        self.user = "sa"
        self.password = "MotDePasseFort123!"
        self.connexion = None
        self.consommation_repo = None
        self.materiel_repo = None
        self.is_connected = False


class SolaireGUI:
    """Interface graphique pour le dimensionnement d'un système solaire avec batterie."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Dimensionnement Système Solaire")
        self.root.geometry("1600x1000")
        self.root.configure(bg="#f0f0f0")
        
        # Configuration base de données
        self.db_config = DatabaseConfig()
        
        # Service pour les calculs
        self.service = None
        self.init_service()
        
        # Données temporaires
        self.materiels = []  # Liste des matériels
        self.consommations = []  # Liste des consommations
        self.configs = {}  # Configurations par période
        
        # Configuration du style
        self.setup_style()
        
        # Création de l'interface
        self.create_widgets()
    
    def init_service(self):
        """Initialise le service avec les repositories appropriés."""
        if self.db_config.is_connected and self.db_config.consommation_repo:
            self.service = ConsommationService(self.db_config.consommation_repo)
        else:
            # Repository dummy si pas de BD
            class RepositoryStub:
                def save(self, obj): return True
                def findAll(self): return []
                def findById(self, id): return None
                def findByMateriel(self, idMateriel): return []
            
            self.service = ConsommationService(RepositoryStub())
    
    def setup_style(self):
        """Configure les styles ttk et couleurs."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Couleurs personnalisées
        self.color_bg = "#f0f0f0"
        self.color_frame = "#ffffff"
        self.color_header = "#2c3e50"
        self.color_accent = "#3498db"
        self.color_success = "#27ae60"
        self.color_warning = "#e74c3c"
        
        style.configure("Header.TLabel", foreground="white", background=self.color_header, 
                       font=("Arial", 12, "bold"), padding=10)
        style.configure("Section.TLabel", font=("Arial", 11, "bold"), foreground=self.color_header)
        style.configure("Normal.TLabel", font=("Arial", 10))
    
    def create_widgets(self):
        """Crée l'interface principale."""
        # Frame de connexion BD en haut
        self.create_db_connection_frame()
        
        # Conteneur principal subdivisant l'espace
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Configure weight pour que le notebook expanding correctement
        main_container.rowconfigure(0, weight=1)  # Notebook prend l'espace
        main_container.rowconfigure(1, weight=0)  # Boutons gardent leur taille
        main_container.columnconfigure(0, weight=1)
        
        # Notebook (onglets) - grid instead de pack pour meilleur contrôle
        notebook = ttk.Notebook(main_container)
        notebook.grid(row=0, column=0, sticky="nsew", pady=10)
        
        # Onglet Configuration
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="📅 Configuration Journée")
        self.create_config_tab(config_frame)
        
        # Onglet Appareils
        appareils_frame = ttk.Frame(notebook)
        notebook.add(appareils_frame, text="⚙️ Appareils Électriques")
        self.create_appareils_tab(appareils_frame)
        
        # Onglet Résultats
        resultats_frame = ttk.Frame(notebook)
        notebook.add(resultats_frame, text="📊 Résultats")
        self.create_resultats_tab(resultats_frame)
        
        # Boutons d'action en bas - sur la deuxième ligne
        self.create_action_buttons(main_container)
    
    def create_db_connection_frame(self):
        """Crée le frame de connexion à la base de données."""
        frame = ttk.LabelFrame(self.root, text="🗄️ Connexion Base de Données", padding="10")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        grid_frame = ttk.Frame(frame)
        grid_frame.pack(fill=tk.X)
        
        # Serveur
        ttk.Label(grid_frame, text="Serveur:", style="Normal.TLabel").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=3)
        serveur_entry = ttk.Entry(grid_frame, width=15)
        serveur_entry.insert(0, self.db_config.serveur)
        serveur_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=3)
        self.serveur_entry = serveur_entry
        
        # DB
        ttk.Label(grid_frame, text="Base:", style="Normal.TLabel").grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=3)
        db_entry = ttk.Entry(grid_frame, width=15)
        db_entry.insert(0, self.db_config.db)
        db_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=3)
        self.db_entry = db_entry
        
        # User
        ttk.Label(grid_frame, text="User:", style="Normal.TLabel").grid(
            row=0, column=4, sticky=tk.W, padx=5, pady=3)
        user_entry = ttk.Entry(grid_frame, width=15)
        user_entry.insert(0, self.db_config.user)
        user_entry.grid(row=0, column=5, sticky=tk.W, padx=5, pady=3)
        self.user_entry = user_entry
        
        # Password
        ttk.Label(grid_frame, text="Password:", style="Normal.TLabel").grid(
            row=0, column=6, sticky=tk.W, padx=5, pady=3)
        password_entry = ttk.Entry(grid_frame, width=15, show="*")
        password_entry.insert(0, self.db_config.password)
        password_entry.grid(row=0, column=7, sticky=tk.W, padx=5, pady=3)
        self.password_entry = password_entry
        
        # Boutons
        ttk.Button(grid_frame, text="🔌 Connexion", 
                  command=self.connecter_bd).grid(row=0, column=8, padx=5, pady=3)
        
        # Statut de connexion
        self.db_status_label = ttk.Label(grid_frame, text="❌ Déconnecté", 
                                         style="Normal.TLabel", foreground="red")
        self.db_status_label.grid(row=0, column=9, padx=5, pady=3)
    
    def connecter_bd(self):
        """Établit la connexion à la base de données."""
        try:
            # Récupérer les paramètres des champs de saisie
            self.db_config.serveur = self.serveur_entry.get()
            self.db_config.db = self.db_entry.get()
            self.db_config.user = self.user_entry.get()
            self.db_config.password = self.password_entry.get()
            
            # Créer la connexion
            self.db_config.connexion = Connexion(
                serve=self.db_config.serveur,
                db=self.db_config.db,
                user=self.db_config.user,
                password=self.db_config.password
            )
            
            # Tester la connexion en exécutant une requête simple
            self.db_config.connexion.connect()
            result = self.db_config.connexion.execute_query("SELECT 1")
            
            # Initialiser les repositories
            self.db_config.consommation_repo = ConsommationRepository(self.db_config.connexion.connection)
            self.db_config.materiel_repo = MaterielRepository(self.db_config.connexion.connection)
            
            # Mettre à jour le statut
            self.db_config.is_connected = True
            self.init_service()  # Réinitialiser le service avec la vraie BD
            
            # Mettre à jour l'UI
            self.db_status_label.config(text="✅ Connecté", foreground="green")
            messagebox.showinfo("Succès", "Connexion à la base de données établie!")
            
        except Exception as e:
            self.db_config.is_connected = False
            self.db_status_label.config(text="❌ Erreur Connexion", foreground="red")
            messagebox.showerror("Erreur", f"Erreur de connexion:\n{str(e)}")
    
    def create_config_tab(self, parent):
        """Crée l'onglet de configuration de la journée."""
        container = ttk.Frame(parent, padding="15")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title = ttk.Label(container, text="Configuration des Périodes de la Journée", 
                         style="Header.TLabel")
        title.pack(fill=tk.X, pady=(0, 15))
        
        # Créer trois sections : Matin, Après-midi, Soir
        self.period_frames = {}
        self.period_inputs = {}
        
        for period_idx, period_name in enumerate(["🌅 MATIN", "☀️ FIN D'APRÈS-MIDI", "🌙 SOIR"]):
            self.create_period_frame(container, period_name, period_idx)
        
        # Frame d'entrée batterie
        battery_frame = self.create_battery_frame(container)
    
    def create_period_frame(self, parent, period_label, period_idx):
        """Crée un frame pour une période de la journée."""
        period_key = ["matin", "apres_midi", "soir"][period_idx]
        
        frame = ttk.LabelFrame(parent, text=period_label, padding="10")
        frame.pack(fill=tk.X, pady=10, padx=5)
        
        self.period_frames[period_key] = frame
        self.period_inputs[period_key] = {}
        
        # Grille 2x2
        grid_frame = ttk.Frame(frame)
        grid_frame.pack(fill=tk.X)
        
        # Heure Début
        ttk.Label(grid_frame, text="Heure Début (HH:MM:SS):", style="Normal.TLabel").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        heure_debut = ttk.Entry(grid_frame, width=20)
        heure_debut.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.period_inputs[period_key]['heure_debut'] = heure_debut
        
        # Heure Fin
        ttk.Label(grid_frame, text="Heure Fin (HH:MM:SS):", style="Normal.TLabel").grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=5)
        heure_fin = ttk.Entry(grid_frame, width=20)
        heure_fin.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        self.period_inputs[period_key]['heure_fin'] = heure_fin
        
        # Rendement
        ttk.Label(grid_frame, text="Rendement (%):", style="Normal.TLabel").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5)
        rendement = ttk.Entry(grid_frame, width=20)
        rendement.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.period_inputs[period_key]['rendement'] = rendement
        
        # Valeur par défaut
        if period_idx == 0:  # Matin
            heure_debut.insert(0, "06:00:00")
            heure_fin.insert(0, "12:00:00")
            rendement.insert(0, "40")
        elif period_idx == 1:  # Après-midi
            heure_debut.insert(0, "12:00:00")
            heure_fin.insert(0, "18:00:00")
            rendement.insert(0, "100")
        else:  # Soir
            heure_debut.insert(0, "18:00:00")
            heure_fin.insert(0, "22:00:00")
            rendement.insert(0, "0")
    
    def create_battery_frame(self, parent):
        """Crée le frame pour la configuration de la batterie."""
        frame = ttk.LabelFrame(parent, text="🔋 Configuration Batterie", padding="10")
        frame.pack(fill=tk.X, pady=10, padx=5)
        
        grid_frame = ttk.Frame(frame)
        grid_frame.pack(fill=tk.X)
        
        # Heure Début Charge
        ttk.Label(grid_frame, text="Heure Début Charge (HH:MM:SS):", 
                 style="Normal.TLabel").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        charge_debut = ttk.Entry(grid_frame, width=20)
        charge_debut.insert(0, "06:00:00")
        charge_debut.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.charge_debut = charge_debut
        
        # Heure Fin Charge
        ttk.Label(grid_frame, text="Heure Fin Charge (HH:MM:SS):", 
                 style="Normal.TLabel").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        charge_fin = ttk.Entry(grid_frame, width=20)
        charge_fin.insert(0, "12:00:00")
        charge_fin.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        self.charge_fin = charge_fin
        
        # Marge Sécurité Batterie
        ttk.Label(grid_frame, text="Marge Sécurité (%):", 
                 style="Normal.TLabel").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        marge = ttk.Entry(grid_frame, width=20)
        marge.insert(0, "50")
        marge.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.marge_batterie = marge
        
        # Info: Capacité calculée automatiquement
        info_label = ttk.Label(grid_frame, 
                              text="ℹ️ Capacité batterie calculée automatiquement basée sur les appareils du soir",
                              style="Normal.TLabel", foreground="gray")
        info_label.grid(row=1, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)
    
    def create_appareils_tab(self, parent):
        """Crée l'onglet de gestion des appareils."""
        container = ttk.Frame(parent, padding="15")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title = ttk.Label(container, text="Gestion des Appareils Électriques", 
                         style="Header.TLabel")
        title.pack(fill=tk.X, pady=(0, 15))
        
        # Frame d'ajout
        add_frame = ttk.LabelFrame(container, text="➕ Ajouter un Appareil", padding="10")
        add_frame.pack(fill=tk.X, pady=10)
        
        grid_frame = ttk.Frame(add_frame)
        grid_frame.pack(fill=tk.X)
        
        # Nom Matériel
        ttk.Label(grid_frame, text="Nom Appareil:", style="Normal.TLabel").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_nom = ttk.Entry(grid_frame, width=20)
        self.input_nom.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Consommation (W)
        ttk.Label(grid_frame, text="Consommation (W):", style="Normal.TLabel").grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.input_puissance = ttk.Entry(grid_frame, width=20)
        self.input_puissance.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Heure Début
        ttk.Label(grid_frame, text="Heure Début (HH:MM:SS):", style="Normal.TLabel").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_heure_debut = ttk.Entry(grid_frame, width=20)
        self.input_heure_debut.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Heure Fin
        ttk.Label(grid_frame, text="Heure Fin (HH:MM:SS):", style="Normal.TLabel").grid(
            row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.input_heure_fin = ttk.Entry(grid_frame, width=20)
        self.input_heure_fin.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Bouton Ajouter
        btn_ajouter = ttk.Button(grid_frame, text="Ajouter", command=self.ajouter_appareil)
        btn_ajouter.grid(row=2, column=0, columnspan=4, pady=10, sticky=tk.W)
        
        # Frame liste des appareils
        list_frame = ttk.LabelFrame(container, text="📋 Liste des Appareils", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview
        columns = ("Nom", "Consommation (W)", "Heure Début", "Heure Fin")
        self.tree_appareils = ttk.Treeview(list_frame, columns=columns, height=10)
        self.tree_appareils.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree_appareils.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_appareils.configure(yscroll=scrollbar.set)
        
        # Configuration des colonnes
        self.tree_appareils.column("#0", width=0, stretch=tk.NO)
        for col in columns:
            self.tree_appareils.column(col, anchor=tk.W, width=200)
            self.tree_appareils.heading(col, text=col, anchor=tk.W)
        
        # Bouton Supprimer
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="❌ Supprimer Sélectionné", 
                  command=self.supprimer_appareil).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Supprimer Tous", 
                  command=self.supprimer_tous).pack(side=tk.LEFT, padx=5)
    
    def create_resultats_tab(self, parent):
        """Crée l'onglet d'affichage des résultats."""
        container = ttk.Frame(parent, padding="15")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title = ttk.Label(container, text="Résultats du Dimensionnement", 
                         style="Header.TLabel")
        title.pack(fill=tk.X, pady=(0, 15))
        
        # Frame résultats
        self.resultats_frame = ttk.Frame(container)
        self.resultats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message initial
        msg = ttk.Label(self.resultats_frame, 
                       text="Cliquez sur 'Calculer' pour voir les résultats", 
                       style="Normal.TLabel", foreground="gray")
        msg.pack(pady=50)
    
    def create_action_buttons(self, parent):
        """Crée les boutons d'action en bas de l'interface."""
        btn_frame = ttk.LabelFrame(parent, text="🎛️ Actions", padding="15")
        btn_frame.grid(row=1, column=0, sticky="ew", pady=15, padx=5)
        
        # Première ligne: Boutons BD
        row1 = ttk.Frame(btn_frame)
        row1.pack(fill=tk.X, pady=8)
        
        ttk.Button(row1, text="💾 Sauvegarder BD", width=25,
                  command=self.sauvegarder_bd).pack(side=tk.LEFT, padx=8)
        ttk.Button(row1, text="📂 Charger BD", width=25,
                  command=self.charger_bd).pack(side=tk.LEFT, padx=8)
        
        # Deuxième ligne: Calcul et Réinitialiser
        row2 = ttk.Frame(btn_frame)
        row2.pack(fill=tk.X, pady=8)
        
        ttk.Button(row2, text="🧮 CALCULER", width=25,
                  command=self.calculer).pack(side=tk.LEFT, padx=8)
        ttk.Button(row2, text="🔄 Réinitialiser", width=25,
                  command=self.reinitialiser).pack(side=tk.LEFT, padx=8)
        
        # Troisième ligne: Quitter
        row3 = ttk.Frame(btn_frame)
        row3.pack(fill=tk.X, pady=8)
        
        ttk.Button(row3, text="❌ QUITTER", width=58,
                  command=self.root.quit).pack(side=tk.LEFT, padx=8)
    
    def ajouter_appareil(self):
        """Ajoute un appareil à la liste."""
        try:
            nom = self.input_nom.get().strip()
            puissance = float(self.input_puissance.get())
            heure_debut = self.input_heure_debut.get().strip()
            heure_fin = self.input_heure_fin.get().strip()
            
            if not nom:
                messagebox.showerror("Erreur", "Le nom de l'appareil est requis")
                return
            
            # Validation des heures
            try:
                time.fromisoformat(heure_debut)
                time.fromisoformat(heure_fin)
            except ValueError:
                messagebox.showerror("Erreur", "Format d'heure invalide. Utilisez HH:MM:SS")
                return
            
            # Ajouter à la liste
            materiel = Materiel(nom=nom)
            self.materiels.append(materiel)
            
            # Créer une consommation
            # Pour le premier matériel, on utilise l'ID 1
            materiel_id = len(self.materiels)
            consommation = Consommation(
                id=len(self.consommations) + 1,
                idMateriel=materiel_id,
                puissance=puissance,
                heureDebut=heure_debut,
                heureFin=heure_fin
            )
            self.consommations.append(consommation)
            
            # Ajouter à la treeview
            self.tree_appareils.insert("", tk.END, 
                                      values=(nom, f"{puissance:.2f}", heure_debut, heure_fin))
            
            # Réinitialiser les inputs
            self.input_nom.delete(0, tk.END)
            self.input_puissance.delete(0, tk.END)
            self.input_heure_debut.delete(0, tk.END)
            self.input_heure_fin.delete(0, tk.END)
            
            messagebox.showinfo("Succès", f"Appareil '{nom}' ajouté avec succès")
            
        except ValueError as e:
            messagebox.showerror("Erreur", f"Valeur invalide: {e}")
    
    def supprimer_appareil(self):
        """Supprime l'appareil sélectionné."""
        selection = self.tree_appareils.selection()
        if selection:
            item = selection[0]
            index = self.tree_appareils.index(item)
            self.tree_appareils.delete(item)
            if index < len(self.materiels):
                self.materiels.pop(index)
            if index < len(self.consommations):
                self.consommations.pop(index)
    
    def supprimer_tous(self):
        """Supprime tous les appareils."""
        if messagebox.askyesno("Confirmation", "Supprimer tous les appareils?"):
            for item in self.tree_appareils.get_children():
                self.tree_appareils.delete(item)
            self.materiels.clear()
            self.consommations.clear()
    
    def calculer(self):
        """Lance le calcul du dimensionnement."""
        try:
            # Valider les configurations
            if not self.materiels or not self.consommations:
                messagebox.showerror("Erreur", "Veuillez ajouter au moins un appareil")
                return
            
            # Créer les ConfigJournee
            configs = {}
            for period_key, period_name in [("matin", "Matin"), 
                                           ("apres_midi", "Après-midi"), 
                                           ("soir", "Soir")]:
                inputs = self.period_inputs[period_key]
                heure_debut = inputs['heure_debut'].get().strip()
                heure_fin = inputs['heure_fin'].get().strip()
                rendement = float(inputs['rendement'].get())
                
                try:
                    hd = datetime.strptime(heure_debut, "%H:%M:%S")
                    hf = datetime.strptime(heure_fin, "%H:%M:%S")
                except ValueError:
                    messagebox.showerror("Erreur", f"Format d'heure invalide pour {period_name}")
                    return
                
                config = ConfigJournee(
                    id=0,
                    heureDebut=hd.time(),
                    heureFin=hf.time(),
                    rendement=rendement,
                    idStatut=0
                )
                configs[period_key] = config
            
            # Paramètres batterie
            charge_debut = self.charge_debut.get().strip()
            charge_fin = self.charge_fin.get().strip()
            marge = float(self.marge_batterie.get()) / 100
            
            # Calculer automatiquement la capacité batterie basée sur les appareils du soir
            soir_inputs = self.period_inputs['soir']
            heure_soir_debut = soir_inputs['heure_debut'].get().strip()
            heure_soir_fin = soir_inputs['heure_fin'].get().strip()
            
            # Calculer la capacité batterie en tenant compte des chevauchements d'appareils
            soir_debut_dt = datetime.strptime(heure_soir_debut, "%H:%M:%S")
            soir_fin_dt = datetime.strptime(heure_soir_fin, "%H:%M:%S")
            soir_debut_time = soir_debut_dt.time()
            soir_fin_time = soir_fin_dt.time()
            
            # Créer une liste d'événements (début/fin) pour les appareils du soir
            evenements = []
            consommations_soir = []
            
            for consommation in self.consommations:
                app_debut = datetime.strptime(consommation.heureDebut, "%H:%M:%S").time()
                app_fin = datetime.strptime(consommation.heureFin, "%H:%M:%S").time()
                
                # Vérifier si l'appareil chevauche le soir
                if app_debut < soir_fin_time and app_fin > soir_debut_time:
                    # Restreindre à la plage soir
                    debut_effectif = max(app_debut, soir_debut_time)
                    fin_effectif = min(app_fin, soir_fin_time)
                    
                    consommations_soir.append({
                        'puissance': consommation.puissance,
                        'debut': debut_effectif,
                        'fin': fin_effectif
                    })
                    
                    evenements.append({'temps': debut_effectif, 'type': 'debut', 'puissance': consommation.puissance})
                    evenements.append({'temps': fin_effectif, 'type': 'fin', 'puissance': consommation.puissance})
            
            # Trier les événements par heure
            evenements.sort(key=lambda x: (x['temps'].hour * 3600 + x['temps'].minute * 60 + x['temps'].second))
            
            # Calculer la capacité en parcourant les intervalles
            capacite = 0
            puissance_active = 0
            
            for i, event in enumerate(evenements):
                if event['type'] == 'debut':
                    puissance_active += event['puissance']
                else:
                    puissance_active -= event['puissance']
                
                # Calculer l'énergie jusqu'au prochain événement
                if i < len(evenements) - 1:
                    heure_debut = event['temps']
                    heure_fin = evenements[i + 1]['temps']
                    
                    secs_debut = heure_debut.hour * 3600 + heure_debut.minute * 60 + heure_debut.second
                    secs_fin = heure_fin.hour * 3600 + heure_fin.minute * 60 + heure_fin.second
                    
                    temps_secondes = secs_fin - secs_debut
                    temps_heures = temps_secondes / 3600
                    
                    energie_wh = puissance_active * temps_heures
                    capacite += energie_wh
            
            # Si aucun appareil le soir, utiliser une valeur par défaut
            if capacite == 0:
                capacite = 100
            
            # Lancer le calcul
            resultats = self.service.dimensionnerSystemeSolaire(
                self.consommations,
                configs['matin'],
                configs['apres_midi'],
                charge_debut,
                charge_fin,
                capacite,
                marge
            )
            
            # Afficher les résultats
            self.afficher_resultats(resultats, configs['matin'].rendement)
            
            messagebox.showinfo("Succès", "Calcul effectué avec succès!")
            
        except Exception as e:
            messagebox.showerror("Erreur lors du calcul", f"{str(e)}")
            import traceback
            traceback.print_exc()
    
    def afficher_resultats(self, resultats, rendement_matin):
        """Affiche les résultats du calcul."""
        # Vider le frame
        for widget in self.resultats_frame.winfo_children():
            widget.destroy()
        
        if resultats is None:
            msg = ttk.Label(self.resultats_frame, text="Erreur lors du calcul", foreground="red")
            msg.pack(pady=50)
            return
        
        # Canvas avec scrollbar
        canvas = tk.Canvas(self.resultats_frame, bg="white", width=1200, height=800)
        scrollbar = ttk.Scrollbar(self.resultats_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Résumé Batterie
        self.create_result_section(scrollable_frame, 
                                   "🔋 BATTERIE",
                                   [
                                       ("Capacité requise", f"{resultats['batterie_capacite']:.2f} Wh"),
                                       ("Puissance pratique", f"{resultats['batterie_puissance_pratique']:.2f} W"),
                                       ("Puissance théorique (à acheter)", f"{resultats['batterie_puissance_theorique']:.2f} W"),
                                       ("Marge de sécurité", f"{resultats['batterie_marge']*100:.0f}%"),
                                       ("Puissance de charge", f"{resultats['batterie_puissance_charge']:.2f} W"),
                                   ])
        
        # Résumé Panneau Solaire
        self.create_result_section(scrollable_frame,
                                   "☀️ PANNEAU SOLAIRE",
                                   [
                                       ("Puissance pratique (utilisable)", f"{resultats['puissance_pratique']:.2f} W"),
                                       ("Puissance théorique (à acheter)", f"{resultats['puissance_theorique']:.2f} W"),
                                       ("Rendement matin", f"{rendement_matin:.0f}%"),
                                       ("Pic puissance matin", f"{resultats['puissance_pratique']:.2f} W"),
                                   ])
        
        # Résumé Couverture
        besoins = resultats['besoins']
        self.create_result_section(scrollable_frame,
                                   "📊 COUVERTURE PAR PÉRIODE",
                                   [
                                       ("Matin (appareils + batterie)", f"{besoins['besoin_matin_pratique']:.2f} W"),
                                       ("Après-midi (appareils seuls)", f"{besoins['besoin_apres_pratique']:.2f} W"),
                                   ])
        
        # Logique de calcul
        logique_color = "green" if resultats['logique'] == "✓ Suffisant" else "orange"
        logique_text = f"Logique: {resultats['logique']}"
        
        logic_frame = ttk.LabelFrame(scrollable_frame, text="✓ NOTATION", padding="10")
        logic_frame.pack(fill=tk.X, padx=10, pady=10)
        
        logic_label = ttk.Label(logic_frame, text=logique_text, 
                               foreground=logique_color)
        logic_label.pack()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_result_section(self, parent, title, items):
        """Crée une section de résultats."""
        frame = ttk.LabelFrame(parent, text=title, padding="10")
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        grid_frame = ttk.Frame(frame)
        grid_frame.pack(fill=tk.X)
        
        for idx, (label, value) in enumerate(items):
            row = idx // 2
            col = (idx % 2) * 2
            
            lbl = ttk.Label(grid_frame, text=f"{label}:", style="Normal.TLabel", 
                           font=("Arial", 10, "bold"))
            lbl.grid(row=row, column=col, sticky=tk.W, padx=5, pady=5)
            
            val = ttk.Label(grid_frame, text=value, style="Normal.TLabel",
                           foreground="#2c3e50", font=("Arial", 10))
            val.grid(row=row, column=col+1, sticky=tk.W, padx=5, pady=5)
    
    def reinitialiser(self):
        """Réinitialise l'interface."""
        if messagebox.askyesno("Confirmation", "Réinitialiser tous les champs?"):
            self.materiels.clear()
            self.consommations.clear()
            
            for item in self.tree_appareils.get_children():
                self.tree_appareils.delete(item)
            
            # Réinitialiser les configurations
            for period_key in self.period_inputs:
                if period_key == "matin":
                    self.period_inputs[period_key]['heure_debut'].delete(0, tk.END)
                    self.period_inputs[period_key]['heure_debut'].insert(0, "06:00:00")
                    self.period_inputs[period_key]['heure_fin'].delete(0, tk.END)
                    self.period_inputs[period_key]['heure_fin'].insert(0, "12:00:00")
                    self.period_inputs[period_key]['rendement'].delete(0, tk.END)
                    self.period_inputs[period_key]['rendement'].insert(0, "40")
                elif period_key == "apres_midi":
                    self.period_inputs[period_key]['heure_debut'].delete(0, tk.END)
                    self.period_inputs[period_key]['heure_debut'].insert(0, "12:00:00")
                    self.period_inputs[period_key]['heure_fin'].delete(0, tk.END)
                    self.period_inputs[period_key]['heure_fin'].insert(0, "18:00:00")
                    self.period_inputs[period_key]['rendement'].delete(0, tk.END)
                    self.period_inputs[period_key]['rendement'].insert(0, "100")
                else:
                    self.period_inputs[period_key]['heure_debut'].delete(0, tk.END)
                    self.period_inputs[period_key]['heure_debut'].insert(0, "18:00:00")
                    self.period_inputs[period_key]['heure_fin'].delete(0, tk.END)
                    self.period_inputs[period_key]['heure_fin'].insert(0, "22:00:00")
                    self.period_inputs[period_key]['rendement'].delete(0, tk.END)
                    self.period_inputs[period_key]['rendement'].insert(0, "0")
    
    def sauvegarder_bd(self):
        """Sauvegarde les données actuelles dans la base de données."""
        if not self.db_config.is_connected:
            messagebox.showwarning("Avertissement", 
                                  "Veuillez d'abord vous connecter à la base de données.")
            return
        
        try:
            count = 0
            # Sauvegarder tous les appareils du Treeview
            for item in self.tree_appareils.get_children():
                values = self.tree_appareils.item(item)['values']
                nom = values[0]
                puissance = int(float(values[1].replace('W', '')))  # Enlever 'W'
                heure_debut = values[2]
                heure_fin = values[3]
                
                # 1. Créer et sauvegarder le Materiel (seulement le nom)
                materiel = Materiel(nom=nom)
                id_materiel = self.db_config.materiel_repo.saveMateriel(materiel)
                
                if id_materiel:
                    # 2. Créer et sauvegarder la Consommation
                    consommation = Consommation(
                        idMateriel=id_materiel,
                        puissance=puissance,
                        heureDebut=heure_debut,
                        heureFin=heure_fin
                    )
                    success = self.db_config.consommation_repo.save(consommation)
                    if success:
                        count += 1
            
            messagebox.showinfo("Succès", f"{count} appareil(s) sauvegardé(s) dans la base de données!")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde:\n{str(e)}")
    
    def charger_bd(self):
        """Charge les données depuis la base de données."""
        if not self.db_config.is_connected:
            messagebox.showwarning("Avertissement", 
                                  "Veuillez d'abord vous connecter à la base de données.")
            return
        
        try:
            # Vider l'interface
            for item in self.tree_appareils.get_children():
                self.tree_appareils.delete(item)
            
            self.materiels.clear()
            count = 0
            
            # Charger tous les matériels depuis la BD
            materiels = self.db_config.materiel_repo.findAll()
            
            if not materiels:
                messagebox.showinfo("Info", "Aucun appareil en base de données.")
                return
            
            for materiel_tuple in materiels:
                id_materiel = materiel_tuple[0]
                nom_materiel = materiel_tuple[1]
                
                # Charger les consommations de ce matériel
                consommations = self.db_config.consommation_repo.findByMateriel(id_materiel)
                
                if consommations:
                    for conso_tuple in consommations:
                        # conso_tuple = (id, idMateriel, puissance, heureDebut, heureFin)
                        puissance = conso_tuple[2]
                        heure_debut = str(conso_tuple[3])
                        heure_fin = str(conso_tuple[4])
                        
                        # Ajouter au Treeview
                        self.tree_appareils.insert('', tk.END, 
                                                  values=(nom_materiel, 
                                                         f"{puissance}W",
                                                         heure_debut,
                                                         heure_fin))
                        count += 1
            
            messagebox.showinfo("Succès", f"{count} appareil(s) chargé(s) depuis la BD!")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement:\n{str(e)}")


def main():
    """Fonction principale."""
    root = tk.Tk()
    app = SolaireGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
