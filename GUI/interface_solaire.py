import os
import sys
import tkinter as tk
from datetime import time
from tkinter import messagebox, ttk

# Garantit les imports depuis la racine du projet.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Database.Connexion import Connexion
from Models.Batterie import Batterie
from Models.ChargeBatterie import ChargeBatterie
from Models.ConfigJournee import ConfigJournee
from Models.Consommation import Consommation
from Models.Materiel import Materiel
from Models.Ressource import Ressource
from Models.Resultat import Resultat
from Repositories.BatterieRepository import BatterieRepository
from Repositories.ChargeBatterieRepository import ChargeBatterieRepository
from Repositories.ConfigJourneeRepository import ConfigJourneeRepository
from Repositories.ConsommationRepository import ConsommationRepository
from Repositories.MaterielRepository import MaterielRepository
from Repositories.RessourceRepository import RessourceRepository
from Repositories.ResultatRepository import ResultatRepository
from Repositories.StatutRepository import StatutRepository
from Services.BatterieService import BatterieService
from Services.ChargeBatterieService import ChargeBatterieService
from Services.ConfigJourneeService import ConfigJourneeService
from Services.ConsommationService import ConsommationService
from Services.MaterielService import MaterielService
from Services.RessourceService import RessourceService
from Services.ResultatService import ResultatService
from Services.StatutService import StatutService


class SolaireGUI:
    # Palette de couleurs moderne
    COLOR_BG = "#f0f2f5"
    COLOR_PRIMARY = "#2c3e50"
    COLOR_ACCENT = "#3498db"
    COLOR_SUCCESS = "#27ae60"
    COLOR_WARNING = "#f39c12"
    COLOR_DANGER = "#e74c3c"
    COLOR_TEXT = "#2c3e50"
    COLOR_LIGHT = "#ecf0f1"
    COLOR_FRAME = "#ffffff"
    
    def __init__(self, root):
        self.root = root
        self.root.title("Solaire - Système de Dimensionnement")
        self.root.geometry("1400x850")
        self.root.configure(bg=self.COLOR_BG)
        
        # Configuration style ttk
        self._setup_styles()

        self.connexion = None
        self.sql_connection = None

        self.materiel_service = None
        self.consommation_service = None
        self.config_service = None
        self.statut_service = None
        self.ressource_service = None
        self.batterie_service = None
        self.charge_service = None
        self.resultat_service = None

        self.materiel_name_to_id = {}
        self.statut_name_to_id = {}
        self.config_label_to_id = {}

        self._build_ui()

    def _setup_styles(self):
        """Configure les styles ttk globaux"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style pour les notebooks
        style.configure('TNotebook', background=self.COLOR_BG, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 12], font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab', 
                  background=[('selected', self.COLOR_ACCENT)],
                  foreground=[('selected', 'white')])
        
        # Style pour les frames
        style.configure('TFrame', background=self.COLOR_BG)
        style.configure('Card.TFrame', background=self.COLOR_FRAME, relief='flat')
        
        # Style pour les labels
        style.configure('TLabel', background=self.COLOR_BG, foreground=self.COLOR_TEXT, font=('Segoe UI', 9))
        style.configure('Title.TLabel', font=('Segoe UI', 12, 'bold'), foreground=self.COLOR_PRIMARY)
        style.configure('Subtitle.TLabel', font=('Segoe UI', 10, 'bold'), foreground=self.COLOR_ACCENT)
        
        # Style pour les boutons
        style.configure('TButton', font=('Segoe UI', 9, 'bold'), padding=[8, 6])
        style.map('TButton',
                  background=[('active', self.COLOR_ACCENT)],
                  foreground=[('active', 'white')])
        
        style.configure('Primary.TButton', font=('Segoe UI', 9, 'bold'))
        style.map('Primary.TButton',
                  background=[('active', self.COLOR_SUCCESS)],
                  foreground=[('active', 'white')])
        
        # Style pour les entries
        style.configure('TEntry', fieldbackground='white', borderwidth=1, relief='solid')
        
        # Style pour les treeviews
        style.configure('Treeview', 
                       font=('Segoe UI', 9),
                       rowheight=25,
                       background=self.COLOR_FRAME,
                       fieldbackground=self.COLOR_FRAME)
        style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'), background=self.COLOR_PRIMARY, foreground='white')
        style.map('Treeview', background=[('selected', self.COLOR_ACCENT)], foreground=[('selected', 'white')])

    def _build_ui(self):
        # Ajouter un header
        header = tk.Frame(self.root, bg=self.COLOR_PRIMARY, height=70)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="☀️ Solaire - Système de Dimensionnement", 
                        font=('Segoe UI', 18, 'bold'), 
                        bg=self.COLOR_PRIMARY, fg='white', pady=20)
        title.pack()
        
        # Notebook avec meilleur padding
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        self.tab_connexion = ttk.Frame(self.notebook)
        self.tab_materiel = ttk.Frame(self.notebook)
        self.tab_consommation = ttk.Frame(self.notebook)
        self.tab_config = ttk.Frame(self.notebook)
        self.tab_ressource = ttk.Frame(self.notebook)
        self.tab_batterie = ttk.Frame(self.notebook)
        self.tab_calcul = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_connexion, text="🔌 Connexion")
        self.notebook.add(self.tab_materiel, text="🔧 Matériels")
        self.notebook.add(self.tab_consommation, text="⚡ Consommations")
        self.notebook.add(self.tab_config, text="⚙️ Config & Statut")
        self.notebook.add(self.tab_ressource, text="☀️ Ressources")
        self.notebook.add(self.tab_batterie, text="🔋 Batteries")
        self.notebook.add(self.tab_calcul, text="📊 Calcul Solaire")

        self._build_tab_connexion()
        self._build_tab_materiel()
        self._build_tab_consommation()
        self._build_tab_config()
        self._build_tab_ressource()
        self._build_tab_batterie()
        self._build_tab_calcul()

    def _build_tab_connexion(self):
        main_frame = ttk.Frame(self.tab_connexion, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Card pour la connexion
        conn_frame = tk.Frame(main_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        conn_frame.pack(fill=tk.X, pady=10)
        
        title = tk.Label(conn_frame, text="Informations de Connexion", 
                        font=('Segoe UI', 11, 'bold'),
                        bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        title.pack()
        
        form_frame = ttk.Frame(conn_frame)
        form_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(form_frame, text="Serveur (ex: 127.0.0.1,1433)", style='TLabel').grid(row=0, column=0, sticky="w", pady=8)
        ttk.Label(form_frame, text="Base de données", style='TLabel').grid(row=1, column=0, sticky="w", pady=8)
        ttk.Label(form_frame, text="Utilisateur", style='TLabel').grid(row=2, column=0, sticky="w", pady=8)
        ttk.Label(form_frame, text="Mot de passe", style='TLabel').grid(row=3, column=0, sticky="w", pady=8)

        self.entry_server = ttk.Entry(form_frame, width=40, font=('Segoe UI', 10))
        self.entry_db = ttk.Entry(form_frame, width=40, font=('Segoe UI', 10))
        self.entry_user = ttk.Entry(form_frame, width=40, font=('Segoe UI', 10))
        self.entry_password = ttk.Entry(form_frame, width=40, font=('Segoe UI', 10), show="•")

        self.entry_server.grid(row=0, column=1, padx=15, pady=8)
        self.entry_db.grid(row=1, column=1, padx=15, pady=8)
        self.entry_user.grid(row=2, column=1, padx=15, pady=8)
        self.entry_password.grid(row=3, column=1, padx=15, pady=8)

        self.entry_server.insert(0, "127.0.0.1,1433")
        self.entry_db.insert(0, "Solaris")
        self.entry_user.insert(0, "sa")
        self.entry_password.insert(0, "MotDePasseFort123!")

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="✓ Connecter", command=self.connect_db).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Charger toutes les données", command=self.refresh_all).pack(side=tk.LEFT, padx=5)

        self.connection_status = tk.StringVar(value="● Non connecté")
        status_label = tk.Label(conn_frame, textvariable=self.connection_status, 
                               font=('Segoe UI', 10, 'bold'), bg=self.COLOR_FRAME, 
                               fg=self.COLOR_DANGER, pady=10)
        status_label.pack()

    def _build_tab_materiel(self):
        main_frame = ttk.Frame(self.tab_materiel, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Formulaire d'ajout/modification
        form_card = tk.Frame(main_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        form_card.pack(fill=tk.X, pady=10)
        
        title = tk.Label(form_card, text="Ajouter / Modifier Matériel", 
                        font=('Segoe UI', 11, 'bold'),
                        bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        title.pack()
        
        form = ttk.Frame(form_card)
        form.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(form, text="Nom du matériel", style='TLabel').grid(row=0, column=0, sticky="w", pady=6)
        self.entry_materiel_nom = ttk.Entry(form, width=34, font=('Segoe UI', 10))
        self.entry_materiel_nom.grid(row=0, column=1, padx=15, pady=6)

        ttk.Label(form, text="ID (pour mise à jour)", style='TLabel').grid(row=1, column=0, sticky="w", pady=6)
        self.entry_materiel_id = ttk.Entry(form, width=14, font=('Segoe UI', 10))
        self.entry_materiel_id.grid(row=1, column=1, sticky="w", padx=15, pady=6)

        button_frame = ttk.Frame(form)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        ttk.Button(button_frame, text="➕ Ajouter", command=self.add_materiel).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="✏️ Modifier", command=self.update_materiel).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Actualiser", command=self.refresh_materiels).pack(side=tk.LEFT, padx=5)

        # Liste des matériels
        list_card = tk.Frame(main_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        list_card.pack(fill=tk.BOTH, expand=True, pady=10)
        
        list_title = tk.Label(list_card, text="Liste des Matériels", 
                             font=('Segoe UI', 11, 'bold'),
                             bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        list_title.pack()

        tree_frame = ttk.Frame(list_card)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_materiels = ttk.Treeview(tree_frame, columns=("id", "nom"), show="headings", height=14)
        self.tree_materiels.heading("id", text="ID")
        self.tree_materiels.heading("nom", text="Nom du Matériel")
        self.tree_materiels.column("id", width=80)
        self.tree_materiels.column("nom", width=400)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_materiels.yview)
        self.tree_materiels.configure(yscroll=scrollbar.set)
        
        self.tree_materiels.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab_consommation(self):
        main_frame = ttk.Frame(self.tab_consommation, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Formulaire d'entrée
        form_card = tk.Frame(main_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        form_card.pack(fill=tk.X, pady=10)
        
        title = tk.Label(form_card, text="Enregistrer une Consommation", 
                        font=('Segoe UI', 11, 'bold'),
                        bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        title.pack()
        
        form = ttk.Frame(form_card)
        form.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(form, text="Matériel", style='TLabel').grid(row=0, column=0, sticky="w", pady=6)
        self.combo_conso_materiel = ttk.Combobox(form, state="readonly", width=28, font=('Segoe UI', 10))
        self.combo_conso_materiel.grid(row=0, column=1, padx=15, pady=6)

        ttk.Label(form, text="Puissance (W)", style='TLabel').grid(row=0, column=2, sticky="w", pady=6)
        self.entry_conso_puissance = ttk.Entry(form, width=14, font=('Segoe UI', 10))
        self.entry_conso_puissance.grid(row=0, column=3, padx=15, pady=6)

        ttk.Label(form, text="Heure début (HH:MM:SS)", style='TLabel').grid(row=1, column=0, sticky="w", pady=6)
        self.entry_conso_debut = ttk.Entry(form, width=14, font=('Segoe UI', 10))
        self.entry_conso_debut.insert(0, "08:00:00")
        self.entry_conso_debut.grid(row=1, column=1, padx=15, pady=6)

        ttk.Label(form, text="Heure fin (HH:MM:SS)", style='TLabel').grid(row=1, column=2, sticky="w", pady=6)
        self.entry_conso_fin = ttk.Entry(form, width=14, font=('Segoe UI', 10))
        self.entry_conso_fin.insert(0, "10:00:00")
        self.entry_conso_fin.grid(row=1, column=3, padx=15, pady=6)

        button_frame = ttk.Frame(form)
        button_frame.grid(row=2, column=0, columnspan=4, pady=15)
        ttk.Button(button_frame, text="💾 Enregistrer", command=self.add_consommation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Actualiser", command=self.refresh_consommations).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📈 Afficher puissances", command=self.show_all_puissances).pack(side=tk.LEFT, padx=5)

        # Liste des consommations
        list_card = tk.Frame(main_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        list_card.pack(fill=tk.BOTH, expand=True, pady=10)
        
        list_title = tk.Label(list_card, text="Liste des Consommations", 
                             font=('Segoe UI', 11, 'bold'),
                             bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        list_title.pack()

        tree_frame = ttk.Frame(list_card)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_consommations = ttk.Treeview(
            tree_frame,
            columns=("id", "idMateriel", "puissance", "heureDebut", "heureFin"),
            show="headings",
            height=14,
        )
        headers = ["ID", "ID Matériel", "Puissance (W)", "Heure début", "Heure fin"]
        for col, label in zip(("id", "idMateriel", "puissance", "heureDebut", "heureFin"), headers):
            self.tree_consommations.heading(col, text=label)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_consommations.yview)
        self.tree_consommations.configure(yscroll=scrollbar.set)
        
        self.tree_consommations.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab_config(self):
        main_frame = ttk.Frame(self.tab_config, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Section supérieure avec deux colonnes
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=10)

        # Statuts
        statut_card = tk.Frame(top_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        statut_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        statut_title = tk.Label(statut_card, text="Statuts de la Journée", 
                               font=('Segoe UI', 11, 'bold'),
                               bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        statut_title.pack()

        tree_frame = ttk.Frame(statut_card)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_statuts = ttk.Treeview(tree_frame, columns=("id", "nom"), show="headings", height=8)
        self.tree_statuts.heading("id", text="ID")
        self.tree_statuts.heading("nom", text="Nom")
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_statuts.yview)
        self.tree_statuts.configure(yscroll=scrollbar.set)
        self.tree_statuts.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(statut_card, text="🔄 Actualiser statuts", command=self.refresh_statuts).pack(anchor="w", padx=10, pady=10)

        # Configuration Journée
        config_card = tk.Frame(top_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        config_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        config_title = tk.Label(config_card, text="Configuration Journée", 
                               font=('Segoe UI', 11, 'bold'),
                               bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        config_title.pack()

        form = ttk.Frame(config_card)
        form.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(form, text="Heure début", style='TLabel').grid(row=0, column=0, sticky="w", pady=6)
        ttk.Label(form, text="Heure fin", style='TLabel').grid(row=1, column=0, sticky="w", pady=6)
        ttk.Label(form, text="Rendement (%)", style='TLabel').grid(row=2, column=0, sticky="w", pady=6)
        ttk.Label(form, text="Statut", style='TLabel').grid(row=3, column=0, sticky="w", pady=6)

        self.entry_config_debut = ttk.Entry(form, width=14, font=('Segoe UI', 10))
        self.entry_config_debut.insert(0, "06:00:00")
        self.entry_config_fin = ttk.Entry(form, width=14, font=('Segoe UI', 10))
        self.entry_config_fin.insert(0, "19:00:00")
        self.entry_config_rendement = ttk.Entry(form, width=14, font=('Segoe UI', 10))
        self.entry_config_rendement.insert(0, "40")
        self.combo_config_statut = ttk.Combobox(form, state="readonly", width=20, font=('Segoe UI', 10))

        self.entry_config_debut.grid(row=0, column=1, padx=10, pady=6)
        self.entry_config_fin.grid(row=1, column=1, padx=10, pady=6)
        self.entry_config_rendement.grid(row=2, column=1, padx=10, pady=6)
        self.combo_config_statut.grid(row=3, column=1, padx=10, pady=6)

        button_frame = ttk.Frame(form)
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)
        ttk.Button(button_frame, text="💾 Enregistrer", command=self.add_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Actualiser", command=self.refresh_configs).pack(side=tk.LEFT, padx=5)

        # Liste des configurations
        list_card = tk.Frame(main_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        list_card.pack(fill=tk.BOTH, expand=True, pady=10)
        
        list_title = tk.Label(list_card, text="Liste des Configurations", 
                             font=('Segoe UI', 11, 'bold'),
                             bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        list_title.pack()

        tree_frame = ttk.Frame(list_card)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_configs = ttk.Treeview(
            tree_frame,
            columns=("id", "heureDebut", "heureFin", "rendement", "idStatut"),
            show="headings",
            height=8,
        )
        for col, label in zip(
            ("id", "heureDebut", "heureFin", "rendement", "idStatut"),
            ("ID", "Heure début", "Heure fin", "Rendement (%)", "ID Statut"),
        ):
            self.tree_configs.heading(col, text=label)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_configs.yview)
        self.tree_configs.configure(yscroll=scrollbar.set)
        self.tree_configs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab_ressource(self):
        main_frame = ttk.Frame(self.tab_ressource, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Ligne supérieure avec deux cartes
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=10)

        # Ressource
        res_card = tk.Frame(top_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        res_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        res_title = tk.Label(res_card, text="Ajouter Ressource", 
                            font=('Segoe UI', 11, 'bold'),
                            bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        res_title.pack()

        res_form = ttk.Frame(res_card)
        res_form.pack(fill=tk.X, padx=20, pady=10)

        # Ligne 1 - Nom
        ttk.Label(res_form, text="Nom de la ressource", style='TLabel').grid(row=0, column=0, sticky="w", pady=8, columnspan=1)
        self.entry_res_nom = ttk.Entry(res_form, width=30, font=('Segoe UI', 10))
        self.entry_res_nom.grid(row=0, column=1, columnspan=2, padx=10, pady=8, sticky="ew")

        # Ligne 2 - Puissance théorique et réelle
        ttk.Label(res_form, text="Puissance théorique (W)", style='TLabel').grid(row=1, column=0, sticky="w", pady=8)
        self.entry_res_theorique = ttk.Entry(res_form, width=14, font=('Segoe UI', 10))
        self.entry_res_theorique.grid(row=1, column=1, padx=10, pady=8)

        ttk.Label(res_form, text="Puissance réelle (W)", style='TLabel').grid(row=1, column=2, sticky="w", pady=8, padx=(10, 0))
        self.entry_res_reelle = ttk.Entry(res_form, width=14, font=('Segoe UI', 10))
        self.entry_res_reelle.grid(row=1, column=3, padx=10, pady=8)

        # Ligne 3 - Rendement
        ttk.Label(res_form, text="Rendement (%)", style='TLabel').grid(row=2, column=0, sticky="w", pady=8)
        self.entry_res_rendement = ttk.Entry(res_form, width=14, font=('Segoe UI', 10))
        self.entry_res_rendement.insert(0, "100")
        self.entry_res_rendement.grid(row=2, column=1, padx=10, pady=8)

        # Ajouter une étiquette explicative
        ttk.Label(res_form, text="Panneau: 40% | Batterie: 75-100%", style='TLabel', foreground="#7f8c8d").grid(row=2, column=2, columnspan=2, sticky="w", padx=10, pady=8)

        # Ligne 4 - Boutons
        res_btn_frame = ttk.Frame(res_form)
        res_btn_frame.grid(row=3, column=0, columnspan=4, pady=15)
        ttk.Button(res_btn_frame, text="💾 Enregistrer", command=self.add_ressource).pack(side=tk.LEFT, padx=5)
        ttk.Button(res_btn_frame, text="🔄 Actualiser", command=self.refresh_ressources).pack(side=tk.LEFT, padx=5)
        
        # Configure column weights for better layout
        res_form.columnconfigure(1, weight=1)

        # Charge Batterie
        charge_card = tk.Frame(top_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        charge_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        charge_title = tk.Label(charge_card, text="Charge de Batterie", 
                               font=('Segoe UI', 11, 'bold'),
                               bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        charge_title.pack()

        charge_form = ttk.Frame(charge_card)
        charge_form.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(charge_form, text="Heure début", style='TLabel').grid(row=0, column=0, sticky="w", pady=6)
        ttk.Label(charge_form, text="Heure fin", style='TLabel').grid(row=1, column=0, sticky="w", pady=6)
        ttk.Label(charge_form, text="Capacité (Wh)", style='TLabel').grid(row=2, column=0, sticky="w", pady=6)
        ttk.Label(charge_form, text="Puissance nécessaire (W)", style='TLabel').grid(row=3, column=0, sticky="w", pady=6)

        self.entry_charge_debut = ttk.Entry(charge_form, width=14, font=('Segoe UI', 10))
        self.entry_charge_debut.insert(0, "10:00:00")
        self.entry_charge_fin = ttk.Entry(charge_form, width=14, font=('Segoe UI', 10))
        self.entry_charge_fin.insert(0, "14:00:00")
        self.entry_charge_capacite = ttk.Entry(charge_form, width=14, font=('Segoe UI', 10))
        self.entry_charge_capacite.insert(0, "240")
        self.entry_charge_puissance = ttk.Entry(charge_form, width=14, font=('Segoe UI', 10))
        self.entry_charge_puissance.insert(0, "60")

        self.entry_charge_debut.grid(row=0, column=1, padx=10, pady=6)
        self.entry_charge_fin.grid(row=1, column=1, padx=10, pady=6)
        self.entry_charge_capacite.grid(row=2, column=1, padx=10, pady=6)
        self.entry_charge_puissance.grid(row=3, column=1, padx=10, pady=6)

        charge_btn_frame = ttk.Frame(charge_form)
        charge_btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        ttk.Button(charge_btn_frame, text="💾 Enregistrer", command=self.add_charge_if_missing).pack(side=tk.LEFT, padx=5)
        ttk.Button(charge_btn_frame, text="🔄 Actualiser", command=self.refresh_charges).pack(side=tk.LEFT, padx=5)

        # Listes en bas
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Ressources
        res_list_card = tk.Frame(bottom_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        res_list_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        res_list_title = tk.Label(res_list_card, text="Liste des Ressources", 
                                 font=('Segoe UI', 11, 'bold'),
                                 bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        res_list_title.pack()

        res_tree_frame = ttk.Frame(res_list_card)
        res_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_ressources = ttk.Treeview(
            res_tree_frame,
            columns=("id", "nom", "theorique", "pratique", "rendement"),
            show="headings",
            height=8,
        )
        for col, label in zip(("id", "nom", "theorique", "pratique", "rendement"), ("ID", "Nom", "Théorique (W)", "Réelle (W)", "Rendement (%)")):
            self.tree_ressources.heading(col, text=label)
        self.tree_ressources.column("id", width=40)
        self.tree_ressources.column("nom", width=120)
        self.tree_ressources.column("theorique", width=100)
        self.tree_ressources.column("pratique", width=100)
        self.tree_ressources.column("rendement", width=80)
        
        scrollbar = ttk.Scrollbar(res_tree_frame, orient=tk.VERTICAL, command=self.tree_ressources.yview)
        self.tree_ressources.configure(yscroll=scrollbar.set)
        self.tree_ressources.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Charges
        charge_list_card = tk.Frame(bottom_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        charge_list_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        charge_list_title = tk.Label(charge_list_card, text="Liste des Charges", 
                                    font=('Segoe UI', 11, 'bold'),
                                    bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        charge_list_title.pack()

        charge_tree_frame = ttk.Frame(charge_list_card)
        charge_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_charges = ttk.Treeview(
            charge_tree_frame,
            columns=("id", "debut", "fin", "capacite", "puissance"),
            show="headings",
            height=8,
        )
        for col, label in zip(
            ("id", "debut", "fin", "capacite", "puissance"),
            ("ID", "Heure début", "Heure fin", "Capacité (Wh)", "Puissance (W)"),
        ):
            self.tree_charges.heading(col, text=label)
        self.tree_charges.column("id", width=50)
        self.tree_charges.column("debut", width=110)
        self.tree_charges.column("fin", width=110)
        self.tree_charges.column("capacite", width=140)
        self.tree_charges.column("puissance", width=120)
        
        scrollbar = ttk.Scrollbar(charge_tree_frame, orient=tk.VERTICAL, command=self.tree_charges.yview)
        self.tree_charges.configure(yscroll=scrollbar.set)
        self.tree_charges.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab_batterie(self):
        main_frame = ttk.Frame(self.tab_batterie, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Formulaire d'ajout/modification
        form_card = tk.Frame(main_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        form_card.pack(fill=tk.X, pady=10)
        
        title = tk.Label(form_card, text="Ajouter / Modifier Batterie", 
                        font=('Segoe UI', 11, 'bold'),
                        bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        title.pack()
        
        form = ttk.Frame(form_card)
        form.pack(fill=tk.X, padx=20, pady=10)

        # Ligne 1 - Capacité théorique et réelle
        ttk.Label(form, text="Capacité théorique (Wh)", style='TLabel').grid(row=0, column=0, sticky="w", pady=8)
        self.entry_batterie_theo = ttk.Entry(form, width=20, font=('Segoe UI', 10))
        self.entry_batterie_theo.grid(row=0, column=1, padx=15, pady=8)

        ttk.Label(form, text="Capacité réelle (Wh)", style='TLabel').grid(row=0, column=2, sticky="w", pady=8, padx=(10, 0))
        self.entry_batterie_reelle = ttk.Entry(form, width=20, font=('Segoe UI', 10))
        self.entry_batterie_reelle.grid(row=0, column=3, padx=15, pady=8)

        # Ligne 2 - Rendement et ID
        ttk.Label(form, text="Rendement (%)", style='TLabel').grid(row=1, column=0, sticky="w", pady=8)
        self.entry_batterie_rendement = ttk.Entry(form, width=20, font=('Segoe UI', 10))
        self.entry_batterie_rendement.insert(0, "100")
        self.entry_batterie_rendement.grid(row=1, column=1, padx=15, pady=8)

        ttk.Label(form, text="ID (pour mise à jour)", style='TLabel').grid(row=1, column=2, sticky="w", pady=8, padx=(10, 0))
        self.entry_batterie_id = ttk.Entry(form, width=20, font=('Segoe UI', 10))
        self.entry_batterie_id.grid(row=1, column=3, padx=15, pady=8)

        # Ligne 3 - Boutons
        button_frame = ttk.Frame(form)
        button_frame.grid(row=2, column=0, columnspan=4, pady=15)
        ttk.Button(button_frame, text="➕ Ajouter", command=self.add_batterie).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="✏️ Modifier", command=self.update_batterie).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Actualiser", command=self.refresh_batteries).pack(side=tk.LEFT, padx=5)

        # Liste des batteries
        list_card = tk.Frame(main_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        list_card.pack(fill=tk.BOTH, expand=True, pady=10)
        
        list_title = tk.Label(list_card, text="Liste des Batteries", 
                             font=('Segoe UI', 11, 'bold'),
                             bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        list_title.pack()

        tree_frame = ttk.Frame(list_card)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_batteries = ttk.Treeview(tree_frame, columns=("id", "theo", "reelle", "rendement"), show="headings", height=14)
        self.tree_batteries.heading("id", text="ID")
        self.tree_batteries.heading("theo", text="Capacité théorique (Wh)")
        self.tree_batteries.heading("reelle", text="Capacité réelle (Wh)")
        self.tree_batteries.heading("rendement", text="Rendement (%)")
        self.tree_batteries.column("id", width=80)
        self.tree_batteries.column("theo", width=200)
        self.tree_batteries.column("reelle", width=200)
        self.tree_batteries.column("rendement", width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_batteries.yview)
        self.tree_batteries.configure(yscroll=scrollbar.set)
        
        self.tree_batteries.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab_calcul(self):
        main_frame = ttk.Frame(self.tab_calcul, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Carte de contrôles
        controls_card = tk.Frame(main_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        controls_card.pack(fill=tk.X, pady=10)
        
        controls_title = tk.Label(controls_card, text="Paramètres de Calcul", 
                                 font=('Segoe UI', 11, 'bold'),
                                 bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        controls_title.pack()
        
        controls = ttk.Frame(controls_card)
        controls.pack(fill=tk.X, padx=20, pady=10)

        # Première ligne
        ttk.Label(controls, text="Heure charge début", style='TLabel').grid(row=0, column=0, sticky="w", pady=8)
        ttk.Label(controls, text="Heure charge fin", style='TLabel').grid(row=0, column=2, sticky="w", pady=8)
        
        self.entry_calc_charge_debut = ttk.Entry(controls, width=12, font=('Segoe UI', 10))
        self.entry_calc_charge_debut.insert(0, "10:00:00")
        self.entry_calc_charge_fin = ttk.Entry(controls, width=12, font=('Segoe UI', 10))
        self.entry_calc_charge_fin.insert(0, "14:00:00")
        
        self.entry_calc_charge_debut.grid(row=0, column=1, padx=10, pady=8)
        self.entry_calc_charge_fin.grid(row=0, column=3, padx=10, pady=8)

        # Deuxième ligne
        ttk.Label(controls, text="Marge batterie (0.50 = 50%)", style='TLabel').grid(row=1, column=0, sticky="w", pady=8)
        self.entry_calc_marge = ttk.Entry(controls, width=12, font=('Segoe UI', 10))
        self.entry_calc_marge.insert(0, "0.50")
        self.entry_calc_marge.grid(row=1, column=1, padx=10, pady=8)
        
        ttk.Label(controls, text="ID Résultat à mettre à jour", style='TLabel').grid(row=1, column=2, sticky="w", pady=8)
        self.entry_calc_resultat_id = ttk.Entry(controls, width=12, font=('Segoe UI', 10))
        self.entry_calc_resultat_id.grid(row=1, column=3, padx=10, pady=8, sticky="w")

        # Troisième ligne - Configurations
        ttk.Label(controls, text="Config matin", style='TLabel').grid(row=2, column=0, sticky="w", pady=8)
        self.combo_calc_config_matin = ttk.Combobox(controls, state="readonly", width=28, font=('Segoe UI', 10))
        self.combo_calc_config_matin.grid(row=2, column=1, padx=10, pady=8, columnspan=1)
        
        ttk.Label(controls, text="Config après-midi", style='TLabel').grid(row=2, column=2, sticky="w", pady=8)
        self.combo_calc_config_apres = ttk.Combobox(controls, state="readonly", width=28, font=('Segoe UI', 10))
        self.combo_calc_config_apres.grid(row=2, column=3, padx=10, pady=8, columnspan=1)

        # Quatrième ligne - Sélection des ressources
        ttk.Label(controls, text="Panneau à utiliser", style='TLabel').grid(row=3, column=0, sticky="w", pady=8)
        self.combo_calc_panneau = ttk.Combobox(controls, state="readonly", width=28, font=('Segoe UI', 10))
        self.combo_calc_panneau.grid(row=3, column=1, padx=10, pady=8, columnspan=1)
        
        ttk.Label(controls, text="Batterie à utiliser", style='TLabel').grid(row=3, column=2, sticky="w", pady=8)
        self.combo_calc_batterie = ttk.Combobox(controls, state="readonly", width=28, font=('Segoe UI', 10))
        self.combo_calc_batterie.grid(row=3, column=3, padx=10, pady=8, columnspan=1)

        # Boutons
        button_frame = ttk.Frame(controls_card)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        ttk.Button(button_frame, text="📊 Analyser et Calculer", command=self.run_dimensionnement).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Recharger tout", command=self.refresh_all).pack(side=tk.LEFT, padx=5)

        # Affichage des résultats
        results_card = tk.Frame(main_frame, bg=self.COLOR_FRAME, relief=tk.RAISED, bd=1)
        results_card.pack(fill=tk.BOTH, expand=True, pady=10)
        
        results_title = tk.Label(results_card, text="Résultats du Calcul Solaire", 
                                font=('Segoe UI', 11, 'bold'),
                                bg=self.COLOR_FRAME, fg=self.COLOR_PRIMARY, pady=10)
        results_title.pack()
        
        text_frame = ttk.Frame(results_card)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.text_resultats = tk.Text(text_frame, wrap="word", height=16, font=('Segoe UI', 10),
                                      bg='#f8f9fa', fg=self.COLOR_TEXT, relief=tk.FLAT, bd=1,
                                      padx=15, pady=12)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_resultats.yview)
        self.text_resultats.configure(yscroll=scrollbar.set)
        
        self.text_resultats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configuration du texte avec couleurs
        self.text_resultats.tag_configure("title", font=('Segoe UI', 10, 'bold'), foreground=self.COLOR_PRIMARY)
        self.text_resultats.tag_configure("success", foreground=self.COLOR_SUCCESS, font=('Segoe UI', 10, 'bold'))
        self.text_resultats.tag_configure("value", foreground=self.COLOR_ACCENT, font=('Segoe UI', 10, 'bold'))

    def _ensure_connected(self):
        if not self.sql_connection:
            messagebox.showerror("Connexion", "Connectez-vous d'abord a la base.")
            return False
        return True

    def _clear_tree(self, tree):
        for row in tree.get_children():
            tree.delete(row)

    def _fmt_time(self, value):
        if value is None:
            return ""
        if isinstance(value, time):
            return value.strftime("%H:%M:%S")
        if hasattr(value, "strftime"):
            return value.strftime("%H:%M:%S")
        return str(value)

    def connect_db(self):
        # Valider que tous les champs sont remplis
        server = self.entry_server.get().strip()
        db = self.entry_db.get().strip()
        user = self.entry_user.get().strip()
        password = self.entry_password.get().strip()
        
        if not server or not db or not user or not password:
            messagebox.showwarning("Connexion", "⚠️ Veuillez remplir tous les champs:\n- Serveur\n- Base de données\n- Utilisateur\n- Mot de passe")
            return
        
        try:
            self.connexion = Connexion(
                serve=server,
                db=db,
                user=user,
                password=password,
            )
            self.connexion.connect()
            self.sql_connection = self.connexion.connection

            if not self.sql_connection:
                raise RuntimeError("Connexion non établie")

            materiel_repo = MaterielRepository(self.sql_connection)
            consommation_repo = ConsommationRepository(self.sql_connection)
            config_repo = ConfigJourneeRepository(self.sql_connection)
            statut_repo = StatutRepository(self.sql_connection)
            ressource_repo = RessourceRepository(self.sql_connection)
            batterie_repo = BatterieRepository(self.sql_connection)
            charge_repo = ChargeBatterieRepository(self.sql_connection)
            resultat_repo = ResultatRepository(self.sql_connection)

            self.materiel_service = MaterielService(materiel_repo)
            self.consommation_service = ConsommationService(consommation_repo)
            self.config_service = ConfigJourneeService(config_repo)
            self.statut_service = StatutService(statut_repo)
            self.ressource_service = RessourceService(ressource_repo)
            self.batterie_service = BatterieService(self.sql_connection)
            self.charge_service = ChargeBatterieService(charge_repo)
            self.resultat_service = ResultatService(resultat_repo)

            self.connection_status.set("● Connecté avec succès")
            self.refresh_all()
            messagebox.showinfo("Connexion", "✓ Connexion réussie à la base de données!")
        except Exception as exc:
            self.connection_status.set("● Erreur de connexion")
            messagebox.showerror("Connexion", f"✗ Échec de connexion:\n{exc}")

    def refresh_all(self):
        if not self._ensure_connected():
            return
        self.refresh_materiels()
        self.refresh_statuts()
        self.refresh_configs()
        self.refresh_consommations()
        self.refresh_ressources()
        self.refresh_batteries()
        self.refresh_charges()
        self.refresh_ressources_combos()

    def refresh_materiels(self):
        if not self._ensure_connected():
            return
        self._clear_tree(self.tree_materiels)
        rows = self.materiel_service.findAll() or []
        self.materiel_name_to_id = {}
        labels = []
        for row in rows:
            rid, nom = row[0], row[1]
            self.tree_materiels.insert("", tk.END, values=(rid, nom))
            self.materiel_name_to_id[nom] = rid
            labels.append(f"{rid} - {nom}")
        self.combo_conso_materiel["values"] = labels
        if labels:
            self.combo_conso_materiel.current(0)

    def add_materiel(self):
        if not self._ensure_connected():
            return
        nom = self.entry_materiel_nom.get().strip()
        if not nom:
            messagebox.showwarning("Materiel", "Nom obligatoire")
            return
        ok = self.materiel_service.saveMateriel(Materiel(nom=nom))
        if ok:
            self.entry_materiel_nom.delete(0, tk.END)
            self.refresh_materiels()
            messagebox.showinfo("Materiel", "Materiel ajoute")
        else:
            messagebox.showerror("Materiel", "Ajout echoue")

    def update_materiel(self):
        if not self._ensure_connected():
            return
        try:
            id_materiel = int(self.entry_materiel_id.get().strip())
        except ValueError:
            messagebox.showwarning("Materiel", "ID materiel invalide")
            return

        nom = self.entry_materiel_nom.get().strip() or None
        ok = self.materiel_service.update(id_materiel, nom=nom)
        if ok:
            self.refresh_materiels()
            messagebox.showinfo("Materiel", "Materiel mis a jour")
        else:
            messagebox.showerror("Materiel", "Update echoue")

    def _selected_materiel_id(self):
        selected = self.combo_conso_materiel.get().strip()
        if not selected or " - " not in selected:
            return None
        return int(selected.split(" - ", 1)[0])

    def add_consommation(self):
        if not self._ensure_connected():
            return
        id_materiel = self._selected_materiel_id()
        if not id_materiel:
            messagebox.showwarning("Consommation", "Selectionner un materiel")
            return

        try:
            puissance = float(self.entry_conso_puissance.get().strip())
        except ValueError:
            messagebox.showwarning("Consommation", "Puissance invalide")
            return

        debut = self.entry_conso_debut.get().strip()
        fin = self.entry_conso_fin.get().strip()

        conso = Consommation(None, id_materiel, puissance, debut, fin)
        ok = self.consommation_service.save(conso)
        if ok:
            self.refresh_consommations()
            messagebox.showinfo("Consommation", "Consommation enregistree")
        else:
            messagebox.showerror("Consommation", "Save echoue")

    def refresh_consommations(self):
        if not self._ensure_connected():
            return
        self._clear_tree(self.tree_consommations)
        rows = self.consommation_service.findAll() or []
        for row in rows:
            self.tree_consommations.insert(
                "",
                tk.END,
                values=(row[0], row[1], row[2], self._fmt_time(row[3]), self._fmt_time(row[4])),
            )

    def show_all_puissances(self):
        if not self._ensure_connected():
            return
        rows = self.consommation_service.findAll() or []
        puissances = [float(row[2]) for row in rows]
        if not puissances:
            messagebox.showinfo("Puissances", "Aucune consommation")
            return

        total = sum(puissances)
        maxi = max(puissances)
        mini = min(puissances)
        msg = f"Toutes les puissances: {puissances}\nTotal: {total:.2f} W\nMin: {mini:.2f} W\nMax: {maxi:.2f} W"
        messagebox.showinfo("Puissances", msg)

    def refresh_statuts(self):
        if not self._ensure_connected():
            return
        self._clear_tree(self.tree_statuts)
        rows = self.statut_service.findAll() or []
        labels = []
        self.statut_name_to_id = {}
        for row in rows:
            rid, nom = row[0], row[1]
            self.tree_statuts.insert("", tk.END, values=(rid, nom))
            labels.append(f"{rid} - {nom}")
            self.statut_name_to_id[nom] = rid
        self.combo_config_statut["values"] = labels
        if labels:
            self.combo_config_statut.current(0)

    def add_config(self):
        if not self._ensure_connected():
            return
        selected = self.combo_config_statut.get().strip()
        if " - " not in selected:
            messagebox.showwarning("Config", "Selectionner un statut")
            return

        id_statut = int(selected.split(" - ", 1)[0])
        debut = self.entry_config_debut.get().strip()
        fin = self.entry_config_fin.get().strip()

        try:
            rendement = float(self.entry_config_rendement.get().strip())
        except ValueError:
            messagebox.showwarning("Config", "Rendement invalide")
            return

        config = ConfigJournee(None, debut, fin, rendement, id_statut)
        ok = self.config_service.save(config)
        if ok:
            self.refresh_configs()
            messagebox.showinfo("Config", "ConfigJournee enregistree")
        else:
            messagebox.showerror("Config", "Save config echoue")

    def refresh_configs(self):
        if not self._ensure_connected():
            return
        self._clear_tree(self.tree_configs)
        rows = self.config_service.findAll() or []
        labels = []
        self.config_label_to_id = {}
        for row in rows:
            label = f"{row[0]} | {self._fmt_time(row[1])}->{self._fmt_time(row[2])} | r={float(row[3]):.2f}"
            self.config_label_to_id[label] = row[0]
            labels.append(label)
            self.tree_configs.insert(
                "",
                tk.END,
                values=(row[0], self._fmt_time(row[1]), self._fmt_time(row[2]), row[3], row[4]),
            )
        self.combo_calc_config_matin["values"] = labels
        self.combo_calc_config_apres["values"] = labels
        if len(labels) >= 1 and not self.combo_calc_config_matin.get():
            self.combo_calc_config_matin.current(0)
        if len(labels) >= 2 and not self.combo_calc_config_apres.get():
            self.combo_calc_config_apres.current(1)
        elif len(labels) == 1 and not self.combo_calc_config_apres.get():
            self.combo_calc_config_apres.current(0)

    def _nullable_float(self, value):
        cleaned = value.strip()
        if not cleaned:
            return None
        return float(cleaned)

    def add_ressource(self):
        if not self._ensure_connected():
            return
        nom = self.entry_res_nom.get().strip()
        if not nom:
            messagebox.showwarning("Ressource", "Nom obligatoire")
            return

        try:
            p_theo = self._nullable_float(self.entry_res_theorique.get())
            p_pratique = self._nullable_float(self.entry_res_reelle.get())
            rendement = self._nullable_float(self.entry_res_rendement.get())
            if rendement is None:
                rendement = 100.0
        except ValueError:
            messagebox.showwarning("Ressource", "Valeurs puissance/rendement invalides")
            return

        res = Ressource(None, nom, p_theo, p_pratique, rendement)
        ok = self.ressource_service.save(res)
        if ok:
            self.refresh_ressources()
            messagebox.showinfo("Ressource", "Ressource enregistrée")
        else:
            messagebox.showerror("Ressource", "Save ressource échoue")

    def refresh_ressources(self):
        if not self._ensure_connected():
            return
        self._clear_tree(self.tree_ressources)
        rows = self.ressource_service.findAll() or []
        for row in rows:
            self.tree_ressources.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4]))

    def refresh_ressources_combos(self):
        """Charge les ressources et batteries disponibles dans les dropdowns"""
        if not self._ensure_connected():
            return
        
        # === PANNEAUX (depuis Ressource) ===
        panneaux_options = []
        ressource_rows = self.ressource_service.findAll() or []
        
        for row in ressource_rows:
            # row: (id, nom, puissanceTheorique, puissanceReelle, rendement)
            resource_id = row[0]
            resource_nom = row[1]
            resource_puissance = row[2] if row[2] is not None else 0
            
            label = f"{resource_id} - {resource_nom} ({resource_puissance}W)"
            panneaux_options.append(label)
        
        # === BATTERIES (depuis Batterie) ===
        batteries_options = []
        batterie_rows = self.batterie_service.findAll() or []
        
        for row in batterie_rows:
            # row: (id, capaciteTheorique, capaciteReelle, rendement)
            batterie_id = row[0]
            capacite_theo = row[1] if row[1] is not None else 0
            rendement = row[3] if row[3] is not None else 100.0
            
            label = f"{batterie_id} - Batterie (théo: {capacite_theo}Wh, rend: {rendement:.0f}%)"
            batteries_options.append(label)
        
        # Mettre à jour les dropdowns
        self.combo_calc_panneau["values"] = panneaux_options
        self.combo_calc_batterie["values"] = batteries_options
        
        # Sélectionner le premier de chaque liste par défaut
        if panneaux_options:
            self.combo_calc_panneau.current(0)
        if batteries_options:
            self.combo_calc_batterie.current(0)

    def add_batterie(self):
        if not self._ensure_connected():
            return
        
        try:
            capacite_theo = self._nullable_float(self.entry_batterie_theo.get())
            capacite_reelle = self._nullable_float(self.entry_batterie_reelle.get())
            rendement = self._nullable_float(self.entry_batterie_rendement.get())
            if rendement is None:
                rendement = 100.0
        except ValueError:
            messagebox.showwarning("Batterie", "Valeurs invalides pour les capacités ou rendement")
            return
        
        batterie = Batterie(
            rendement=rendement,
            capaciteTheorique=capacite_theo,
            capaciteReelle=capacite_reelle
        )
        ok = self.batterie_service.save(batterie)
        if ok:
            self.refresh_batteries()
            self.refresh_ressources_combos()
            # Effacer les champs
            self.entry_batterie_theo.delete(0, tk.END)
            self.entry_batterie_reelle.delete(0, tk.END)
            self.entry_batterie_rendement.delete(0, tk.END)
            self.entry_batterie_rendement.insert(0, "100")
            self.entry_batterie_id.delete(0, tk.END)
            messagebox.showinfo("Batterie", "Batterie enregistrée")
        else:
            messagebox.showerror("Batterie", "Erreur lors de l'enregistrement")

    def update_batterie(self):
        if not self._ensure_connected():
            return
        
        id_str = self.entry_batterie_id.get().strip()
        if not id_str:
            messagebox.showwarning("Batterie", "Veuillez entrer l'ID de la batterie à modifier")
            return
        
        try:
            batterie_id = int(id_str)
            capacite_theo = self._nullable_float(self.entry_batterie_theo.get())
            capacite_reelle = self._nullable_float(self.entry_batterie_reelle.get())
            rendement = self._nullable_float(self.entry_batterie_rendement.get())
        except ValueError:
            messagebox.showwarning("Batterie", "Valeurs invalides pour l'ID ou capacités")
            return
        
        ok = self.batterie_service.update(
            batterie_id,
            capaciteTheorique=capacite_theo,
            capaciteReelle=capacite_reelle,
            rendement=rendement
        )
        if ok:
            self.refresh_batteries()
            self.refresh_ressources_combos()
            messagebox.showinfo("Batterie", "Batterie mise à jour")
        else:
            messagebox.showerror("Batterie", "Erreur lors de la mise à jour")

    def refresh_batteries(self):
        if not self._ensure_connected():
            return
        self._clear_tree(self.tree_batteries)
        rows = self.batterie_service.findAll() or []
        for row in rows:
            # row: (id, capaciteTheorique, capaciteReelle, rendement)
            self.tree_batteries.insert(
                "",
                tk.END,
                values=(row[0], row[1] or "-", row[2] or "-", f"{row[3]:.1f}" if row[3] is not None else "-")
            )

    def add_charge_if_missing(self):
        if not self._ensure_connected():
            return
        debut = self.entry_charge_debut.get().strip()
        fin = self.entry_charge_fin.get().strip()

        try:
            capacite = float(self.entry_charge_capacite.get().strip())
            puissance = float(self.entry_charge_puissance.get().strip())
        except ValueError:
            messagebox.showwarning("Charge", "Capacite/Puissance invalides")
            return

        existing = self.charge_service.findAll() or []
        for row in existing:
            same = (
                self._fmt_time(row[1]) == debut
                and self._fmt_time(row[2]) == fin
                and float(row[3]) == capacite
                and float(row[4]) == puissance
            )
            if same:
                messagebox.showinfo("Charge", "Cette charge existe deja")
                self.refresh_charges()
                return

        charge = ChargeBatterie(heureDebut=debut, heureFin=fin, capacite=capacite, PuisanceNecessaire=puissance)
        ok = self.charge_service.save(charge)
        if ok:
            self.refresh_charges()
            messagebox.showinfo("Charge", "Charge enregistree")
        else:
            messagebox.showerror("Charge", "Save charge echoue")

    def refresh_charges(self):
        if not self._ensure_connected():
            return
        self._clear_tree(self.tree_charges)
        rows = self.charge_service.findAll() or []
        for row in rows:
            self.tree_charges.insert(
                "",
                tk.END,
                values=(row[0], self._fmt_time(row[1]), self._fmt_time(row[2]), row[3], row[4]),
            )

    def _get_config_by_id(self, config_id):
        row = self.config_service.findById(config_id)
        if not row:
            return None
        return ConfigJournee(row[0], row[1], row[2], float(row[3]), row[4])

    def _read_consommations_as_models(self):
        rows = self.consommation_service.findAll() or []
        return [Consommation(r[0], r[1], float(r[2]), self._fmt_time(r[3]), self._fmt_time(r[4])) for r in rows]

    def _upsert_ressource(self, nom, puissance_theorique, puissance_pratique, rendement=100.0):
        matches = self.ressource_service.findByNom(nom) or []
        chosen = None
        for row in matches:
            if row[1].strip().lower() == nom.strip().lower():
                chosen = row
                break

        if chosen:
            self.ressource_service.update(chosen[0], nom=nom, puissanceTheorique=puissance_theorique, puissanceReelle=puissance_pratique, rendement=rendement)
            return chosen[0]

        self.ressource_service.save(Ressource(None, nom, puissance_theorique, puissance_pratique, rendement))
        matches = self.ressource_service.findByNom(nom) or []
        for row in matches:
            if row[1].strip().lower() == nom.strip().lower():
                return row[0]
        return None

    def run_dimensionnement(self):
        if not self._ensure_connected():
            return

        # === RÉCUPÉRER LES RESSOURCES SÉLECTIONNÉES ===
        selected_panneau_text = self.combo_calc_panneau.get().strip()
        selected_batterie_text = self.combo_calc_batterie.get().strip()
        
        if not selected_panneau_text or not selected_batterie_text:
            messagebox.showwarning("Calcul", "Veuillez sélectionner une ressource panneau et batterie")
            return
        
        # Extraire les IDs
        try:
            id_panneau_sel = int(selected_panneau_text.split(" - ")[0])
            id_batterie_sel = int(selected_batterie_text.split(" - ")[0])
        except (ValueError, IndexError):
            messagebox.showerror("Calcul", "Erreur lors du parsing des ressources sélectionnées")
            return
        
        # Récupérer les données complètes des ressources sélectionnées
        ressource_panneau = self.ressource_service.findById(id_panneau_sel)
        ressource_batterie = self.batterie_service.findById(id_batterie_sel)
        
        if not ressource_panneau or not ressource_batterie:
            messagebox.showerror("Calcul", "Ressource sélectionnée introuvable dans la base de données")
            return
        
        # Extraire les rendements et puissances
        # ressource_panneau: (id, nom, puissanceTheorique, puissanceReelle, rendement) - tuple
        # ressource_batterie: objet Batterie avec attributs
        rendement_panneau_sel = float(ressource_panneau[4]) if ressource_panneau[4] is not None else 100.0
        rendement_batterie_sel = float(ressource_batterie.rendement) if ressource_batterie.rendement is not None else 100.0

        consommations = self._read_consommations_as_models()
        if not consommations:
            messagebox.showwarning("Calcul", "Aucune consommation disponible")
            return

        # === MÉTHODE OLD: BATTERIE NUIT SEULEMENT ===
        
        # 1. Batterie nuit (19:00 → 06:00) - cross-midnight
        from datetime import datetime, timedelta
        batterie_nuit = 0.0
        for c in consommations:
            hd_min = datetime.strptime(c.heureDebut, "%H:%M:%S").time()
            hf_min = datetime.strptime(c.heureFin, "%H:%M:%S").time()
            
            # Définir si c'est pendant "la nuit"
            # Nuit = 19:00 → 06:00 (cross-midnight)
            is_night = False
            if hd_min >= datetime.strptime("19:00:00", "%H:%M:%S").time():  # 19:00+
                is_night = True
            elif hf_min <= datetime.strptime("06:00:00", "%H:%M:%S").time():  # Avant 06:00
                is_night = True
            
            if is_night:
                # Durée = (heure fin - heure débit) en heures
                hd_dt = datetime.strptime(c.heureDebut, "%H:%M:%S")
                hf_dt = datetime.strptime(c.heureFin, "%H:%M:%S")
                if hf_dt < hd_dt:  # Cross-midnight
                    hf_dt = hf_dt + timedelta(days=1)
                duration_h = (hf_dt - hd_dt).total_seconds() / 3600.0
                batterie_nuit += c.puissance * duration_h
        
        # 2. Batterie réelle × 1.5
        batterie_reelle = batterie_nuit * 1.5
        
        # 3. Puissance charge = batterie nuit / 12h
        p_charge = batterie_nuit / 12.0
        
        # 4. Puissance max simultanée (pic instantané) - UTILISE SERVICE CORRIGÉ
        res_p_max = self.consommation_service.calculerPuissanceMaxSimultanee(consommations)
        p_max = float(res_p_max.get("puissance_max", 0.0))
        
        # 5. Panneau théorique et rendement - EN TENANT COMPTE DU NERF
        selected_matin = self.combo_calc_config_matin.get().strip()
        selected_apres = self.combo_calc_config_apres.get().strip()
        config_matin_id = self.config_label_to_id.get(selected_matin)
        config_apres_id = self.config_label_to_id.get(selected_apres)
        
        rendement_matin = 0.40  # Default 40% rendement soleil matin
        rendement_apres = 0.40  # Default 40% rendement soleil après-midi (peut être réduit = "nerf")
        
        if config_matin_id:
            cfg = self._get_config_by_id(config_matin_id)
            if cfg:
                rendement_matin = float(cfg.rendement) / 100.0
        
        if config_apres_id:
            cfg = self._get_config_by_id(config_apres_id)
            if cfg:
                rendement_apres = float(cfg.rendement) / 100.0
        
        # Panneau pratique = pic + charge (puissance réelle requise)
        # Le panneau doit fournir: appareils ET charger batterie en même temps
        panneau_pratique = p_max + p_charge
        
        # Rendement technique du panneau (utilise le rendement de la ressource sélectionnée)
        rendement_panneau = rendement_panneau_sel / 100.0
        
        # Panneau théorique = pratique / rendement_panneau
        # (la puissance théorique que le panneau doit avoir pour fournir la puissance pratique)
        panneau_theorique = panneau_pratique / rendement_panneau if rendement_panneau > 0 else 0.0
        
        # Rendement total = rendement_panneau (cette ressource aura ce rendement)
        rendement_ressource_panneau = rendement_panneau_sel
        
        # 6. Besoin matin et midi (pics par tranche horaire)
        besoin_matin = 0.0
        besoin_midi = 0.0

        def _to_dt(value):
            if isinstance(value, str):
                return datetime.strptime(value, "%H:%M:%S")
            return datetime.combine(datetime.today().date(), value)

        times_set = set()
        for c in consommations:
            hd_dt = _to_dt(c.heureDebut)
            hf_dt = _to_dt(c.heureFin)
            if hf_dt < hd_dt:
                hf_dt = hf_dt + timedelta(days=1)
            times_set.add(hd_dt)
            times_set.add(hf_dt)
        
        for t in sorted(times_set):
            power_at_t = 0.0
            for c in consommations:
                hd_dt = _to_dt(c.heureDebut)
                hf_dt = _to_dt(c.heureFin)
                if hf_dt < hd_dt:
                    hf_dt = hf_dt + timedelta(days=1)
                if hd_dt <= t < hf_dt:
                    power_at_t += c.puissance
            
            # Matin: 06:00 → 17:00
            if datetime.strptime("06:00:00", "%H:%M:%S") <= t < datetime.strptime("17:00:00", "%H:%M:%S"):
                besoin_matin = max(besoin_matin, power_at_t)
            # Midi: 17:00 → 19:00
            elif datetime.strptime("17:00:00", "%H:%M:%S") <= t < datetime.strptime("19:00:00", "%H:%M:%S"):
                besoin_midi = max(besoin_midi, power_at_t)
        
        # Sauvegarder la charge
        res_connexion = self.consommation_service.findAll()
        hd = "06:00:00"
        hf = "19:00:00"
        
        charge_calculee = ChargeBatterie(
            heureDebut=hd,
            heureFin=hf,
            capacite=batterie_nuit,
            PuisanceNecessaire=p_charge,
        )
        charges = self.charge_service.findAll() or []
        exists = any(
            self._fmt_time(c[1]) == hd
            and self._fmt_time(c[2]) == hf
            and float(c[3]) == float(batterie_nuit)
            and float(c[4]) == float(p_charge)
            for c in charges
        )
        if not exists:
            self.charge_service.save(charge_calculee)
        
        # Ressources: Mettre à jour les ressources sélectionnées avec les puissances calculées
        # Batterie
        self.batterie_service.update(
            id_batterie_sel,
            capaciteTheorique=batterie_reelle,
            capaciteReelle=batterie_nuit,
            rendement=rendement_batterie_sel
        )
        
        # Panneau
        self.ressource_service.update(
            id_panneau_sel,
            nom=ressource_panneau[1],  # Garder le nom existant
            puissanceTheorique=panneau_theorique,
            puissanceReelle=panneau_pratique,
            rendement=rendement_ressource_panneau
        )
        
        self.refresh_ressources()
        self.refresh_batteries()
        self.refresh_charges()
        
        # Affichage avec meilleur formatage
        self.text_resultats.delete("1.0", tk.END)
        
        # Titre
        self.text_resultats.insert(tk.END, "⚡ CALCUL SOLAIRE - MÉTHODE NUIT SEULEMENT\n", "title")
        self.text_resultats.insert(tk.END, "=" * 50 + "\n\n")
        
        # Section Batterie
        self.text_resultats.insert(tk.END, "🔋 BATTERIE\n", "title")
        self.text_resultats.insert(tk.END, "-" * 50 + "\n")
        self.text_resultats.insert(tk.END, f"  Rendement : ", "")
        self.text_resultats.insert(tk.END, f"{rendement_batterie_sel:.0f}%\n", "value")
        self.text_resultats.insert(tk.END, f"  Batterie (nuit 19:00 → 06:00) : ", "")
        self.text_resultats.insert(tk.END, f"{batterie_nuit:.2f} Wh\n", "value")
        self.text_resultats.insert(tk.END, f"  Batterie réelle (marge ×1.5) : ", "")
        self.text_resultats.insert(tk.END, f"{batterie_reelle:.2f} Wh\n\n", "value")
        
        # Section Charge
        self.text_resultats.insert(tk.END, "⚙️ CHARGE\n", "title")
        self.text_resultats.insert(tk.END, "-" * 50 + "\n")
        self.text_resultats.insert(tk.END, f"  Puissance recharge (÷12h) : ", "")
        self.text_resultats.insert(tk.END, f"{p_charge:.2f} W\n\n", "value")
        
        # Section Besoins
        self.text_resultats.insert(tk.END, "📊 BESOINS ÉNERGÉTIQUES\n", "title")
        self.text_resultats.insert(tk.END, "-" * 50 + "\n")
        self.text_resultats.insert(tk.END, f"  Besoin matin (06:00 → 17:00) : ", "")
        self.text_resultats.insert(tk.END, f"{besoin_matin:.2f} W\n", "value")
        self.text_resultats.insert(tk.END, f"  Besoin après-midi (17:00 → 19:00) : ", "")
        self.text_resultats.insert(tk.END, f"{besoin_midi:.2f} W\n", "value")
        self.text_resultats.insert(tk.END, f"  Pic instantané : ", "")
        self.text_resultats.insert(tk.END, f"{p_max:.2f} W\n\n", "value")
        
        # Section Panneau
        self.text_resultats.insert(tk.END, "☀️ PANNEAU SOLAIRE\n", "title")
        self.text_resultats.insert(tk.END, "-" * 50 + "\n")
        
        # Puissances DU PANNEAU (valeurs calculées et sauvegardées à l'instant)
        # panneau_theorique et panneau_pratique ont été calculés ci-dessus
        panneau_theo_initial = panneau_theorique
        panneau_reel_initial = panneau_pratique
        
        self.text_resultats.insert(tk.END, f"  📌 Panneau sélectionné: {ressource_panneau[1]}\n", "")
        self.text_resultats.insert(tk.END, f"     (ID: {ressource_panneau[0]})\n\n", "")
        
        # Affichage des puissances du panneau
        self.text_resultats.insert(tk.END, f"  📦 PUISSANCE THÉORIQUE (à acheter) : ", "")
        self.text_resultats.insert(tk.END, f"{panneau_theo_initial:.2f} W\n", "value")
        
        self.text_resultats.insert(tk.END, f"  💾 PUISSANCE RÉELLE (fournie matin 40%) : ", "")
        self.text_resultats.insert(tk.END, f"{panneau_reel_initial:.2f} W\n\n", "value")
        
        self.text_resultats.insert(tk.END, f"  Rendement technique du panneau: ", "")
        self.text_resultats.insert(tk.END, f"{rendement_ressource_panneau:.0f}%\n\n", "value")
        
        self.text_resultats.insert(tk.END, f"  Rendement matin (06:00 → 17:00) : ", "")
        self.text_resultats.insert(tk.END, f"{rendement_matin*100:.0f}%\n", "value")
        self.text_resultats.insert(tk.END, f"  Rendement après-midi (17:00 → 19:00) : ", "")
        self.text_resultats.insert(tk.END, f"{rendement_apres*100:.0f}%", "value")
        
        if rendement_apres < rendement_matin:
            self.text_resultats.insert(tk.END, " ⚠️ NERF\n\n", "value")
        else:
            self.text_resultats.insert(tk.END, "\n\n", "value")
        
        self.text_resultats.insert(tk.END, f"  💡 Appareils (pic) : ", "")
        self.text_resultats.insert(tk.END, f"{p_max:.2f} W\n", "value")
        self.text_resultats.insert(tk.END, f"  🔋 Charge batterie : ", "")
        self.text_resultats.insert(tk.END, f"{p_charge:.2f} W\n", "value")
        self.text_resultats.insert(tk.END, f"  ➕ TOTAL (appareils + charge) : ", "")
        self.text_resultats.insert(tk.END, f"{panneau_pratique:.2f} W\n\n", "value")
        
        # Calculer puissance réelle selon l'ensoleillement
        panneau_reel_matin = panneau_theo_initial * rendement_matin
        panneau_reel_apres = panneau_theo_initial * rendement_apres
        
        self.text_resultats.insert(tk.END, f"  ⚡ PUISSANCE RÉELLE FOURNIE (selon ensoleillement):\n", "")
        self.text_resultats.insert(tk.END, f"    - Matin (06:00-17:00, {rendement_matin*100:.0f}%) : ", "")
        self.text_resultats.insert(tk.END, f"{panneau_reel_matin:.2f} W\n", "value")
        self.text_resultats.insert(tk.END, f"    - Après-midi (17:00-19:00, {rendement_apres*100:.0f}%) : ", "")
        self.text_resultats.insert(tk.END, f"{panneau_reel_apres:.2f} W", "value")
        if rendement_apres < rendement_matin:
            self.text_resultats.insert(tk.END, " ⚠️ NERF\n", "value")
        else:
            self.text_resultats.insert(tk.END, "\n", "value")
        
        self.text_resultats.insert(tk.END, f"\n  🎯 Puissance requise (appareils + charge): ", "")
        self.text_resultats.insert(tk.END, f"{panneau_pratique:.2f} W\n\n", "value")
        
        # Vérifications
        if panneau_reel_matin >= panneau_pratique:
            self.text_resultats.insert(tk.END, f"  ✅ Matin: Le panneau peut fournir\n", "success")
        else:
            deficit = panneau_pratique - panneau_reel_matin
            self.text_resultats.insert(tk.END, f"  ⚠️ Matin: Déficit de {deficit:.2f} W\n", "success")
        
        if panneau_reel_apres >= panneau_pratique:
            self.text_resultats.insert(tk.END, f"  ✅ Après-midi: Le panneau peut fournir\n", "success")
        else:
            deficit = panneau_pratique - panneau_reel_apres
            self.text_resultats.insert(tk.END, f"  ⚠️ Après-midi: Déficit de {deficit:.2f} W (batterie doit compenser)\n", "success")
        
        self.text_resultats.insert(tk.END, "✓ Calcul complété et ressources actualisées", "success")


def run():
    root = tk.Tk()
    SolaireGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run()
