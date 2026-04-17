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
from Models.ChargeBatterie import ChargeBatterie
from Models.ConfigJournee import ConfigJournee
from Models.Consommation import Consommation
from Models.Materiel import Materiel
from Models.Ressource import Ressource
from Models.Resultat import Resultat
from Repositories.ChargeBatterieRepository import ChargeBatterieRepository
from Repositories.ConfigJourneeRepository import ConfigJourneeRepository
from Repositories.ConsommationRepository import ConsommationRepository
from Repositories.MaterielRepository import MaterielRepository
from Repositories.RessourceRepository import RessourceRepository
from Repositories.ResultatRepository import ResultatRepository
from Repositories.StatutRepository import StatutRepository
from Services.ChargeBatterieService import ChargeBatterieService
from Services.ConfigJourneeService import ConfigJourneeService
from Services.ConsommationService import ConsommationService
from Services.MaterielService import MaterielService
from Services.RessourceService import RessourceService
from Services.ResultatService import ResultatService
from Services.StatutService import StatutService


class SolaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solaire - Interface de dimensionnement")
        self.root.geometry("1280x760")

        self.connexion = None
        self.sql_connection = None

        self.materiel_service = None
        self.consommation_service = None
        self.config_service = None
        self.statut_service = None
        self.ressource_service = None
        self.charge_service = None
        self.resultat_service = None

        self.materiel_name_to_id = {}
        self.statut_name_to_id = {}
        self.config_label_to_id = {}

        self._build_ui()

    def _build_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.tab_connexion = ttk.Frame(self.notebook)
        self.tab_materiel = ttk.Frame(self.notebook)
        self.tab_consommation = ttk.Frame(self.notebook)
        self.tab_config = ttk.Frame(self.notebook)
        self.tab_ressource = ttk.Frame(self.notebook)
        self.tab_calcul = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_connexion, text="Connexion")
        self.notebook.add(self.tab_materiel, text="Materiels")
        self.notebook.add(self.tab_consommation, text="Consommations")
        self.notebook.add(self.tab_config, text="Config et statut")
        self.notebook.add(self.tab_ressource, text="Ressources et charge")
        self.notebook.add(self.tab_calcul, text="Calcul solaire")

        self._build_tab_connexion()
        self._build_tab_materiel()
        self._build_tab_consommation()
        self._build_tab_config()
        self._build_tab_ressource()
        self._build_tab_calcul()

    def _build_tab_connexion(self):
        frame = ttk.Frame(self.tab_connexion, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Serveur (ex: 127.0.0.1,1433)").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Label(frame, text="Base").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Label(frame, text="Utilisateur").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Label(frame, text="Mot de passe").grid(row=3, column=0, sticky="w", pady=6)

        self.entry_server = ttk.Entry(frame, width=40)
        self.entry_db = ttk.Entry(frame, width=40)
        self.entry_user = ttk.Entry(frame, width=40)
        self.entry_password = ttk.Entry(frame, width=40, show="*")

        self.entry_server.grid(row=0, column=1, padx=10)
        self.entry_db.grid(row=1, column=1, padx=10)
        self.entry_user.grid(row=2, column=1, padx=10)
        self.entry_password.grid(row=3, column=1, padx=10)

        self.entry_server.insert(0, "127.0.0.1,1433")
        self.entry_db.insert(0, "Solaris")
        self.entry_user.insert(0, "sa")
        self.entry_password.insert(0, "MotDePasseFort123!")

        ttk.Button(frame, text="Connecter", command=self.connect_db).grid(row=4, column=0, pady=14)
        ttk.Button(frame, text="Charger toutes les listes", command=self.refresh_all).grid(row=4, column=1, sticky="w", pady=14)

        self.connection_status = tk.StringVar(value="Non connecte")
        ttk.Label(frame, textvariable=self.connection_status, foreground="blue").grid(row=5, column=0, columnspan=2, sticky="w", pady=8)

    def _build_tab_materiel(self):
        frame = ttk.Frame(self.tab_materiel, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)

        form = ttk.LabelFrame(frame, text="Ajouter / modifier materiel", padding=12)
        form.pack(fill=tk.X)

        ttk.Label(form, text="Nom materiel").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_materiel_nom = ttk.Entry(form, width=34)
        self.entry_materiel_nom.grid(row=0, column=1, padx=8, pady=4)

        ttk.Label(form, text="ID (pour update)").grid(row=1, column=0, sticky="w", pady=4)
        self.entry_materiel_id = ttk.Entry(form, width=14)
        self.entry_materiel_id.grid(row=1, column=1, sticky="w", padx=8, pady=4)

        ttk.Button(form, text="Ajouter materiel", command=self.add_materiel).grid(row=2, column=0, pady=8)
        ttk.Button(form, text="Update materiel", command=self.update_materiel).grid(row=2, column=1, sticky="w", pady=8)
        ttk.Button(form, text="Charger findAll", command=self.refresh_materiels).grid(row=2, column=2, padx=8, pady=8)

        list_frame = ttk.LabelFrame(frame, text="Liste materiels (findAll)", padding=12)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree_materiels = ttk.Treeview(list_frame, columns=("id", "nom"), show="headings", height=12)
        self.tree_materiels.heading("id", text="ID")
        self.tree_materiels.heading("nom", text="Nom")
        self.tree_materiels.column("id", width=70)
        self.tree_materiels.column("nom", width=320)
        self.tree_materiels.pack(fill=tk.BOTH, expand=True)

    def _build_tab_consommation(self):
        frame = ttk.Frame(self.tab_consommation, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)

        form = ttk.LabelFrame(frame, text="Entrer consommation", padding=12)
        form.pack(fill=tk.X)

        ttk.Label(form, text="Materiel").grid(row=0, column=0, sticky="w", pady=4)
        self.combo_conso_materiel = ttk.Combobox(form, state="readonly", width=28)
        self.combo_conso_materiel.grid(row=0, column=1, padx=8, pady=4)

        ttk.Label(form, text="Puissance (W)").grid(row=0, column=2, sticky="w", pady=4)
        self.entry_conso_puissance = ttk.Entry(form, width=12)
        self.entry_conso_puissance.grid(row=0, column=3, padx=8, pady=4)

        ttk.Label(form, text="Heure debut (HH:MM:SS)").grid(row=1, column=0, sticky="w", pady=4)
        self.entry_conso_debut = ttk.Entry(form, width=14)
        self.entry_conso_debut.insert(0, "08:00:00")
        self.entry_conso_debut.grid(row=1, column=1, padx=8, pady=4)

        ttk.Label(form, text="Heure fin (HH:MM:SS)").grid(row=1, column=2, sticky="w", pady=4)
        self.entry_conso_fin = ttk.Entry(form, width=14)
        self.entry_conso_fin.insert(0, "10:00:00")
        self.entry_conso_fin.grid(row=1, column=3, padx=8, pady=4)

        ttk.Button(form, text="Save consommation", command=self.add_consommation).grid(row=2, column=0, pady=8)
        ttk.Button(form, text="Charger findAll", command=self.refresh_consommations).grid(row=2, column=1, sticky="w", pady=8)
        ttk.Button(form, text="Trouver toutes puissances", command=self.show_all_puissances).grid(row=2, column=2, sticky="w", pady=8)

        list_frame = ttk.LabelFrame(frame, text="Liste consommations", padding=12)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree_consommations = ttk.Treeview(
            list_frame,
            columns=("id", "idMateriel", "puissance", "heureDebut", "heureFin"),
            show="headings",
            height=12,
        )
        headers = ["ID", "ID Materiel", "Puissance", "Heure debut", "Heure fin"]
        for col, label in zip(("id", "idMateriel", "puissance", "heureDebut", "heureFin"), headers):
            self.tree_consommations.heading(col, text=label)
        self.tree_consommations.pack(fill=tk.BOTH, expand=True)

    def _build_tab_config(self):
        frame = ttk.Frame(self.tab_config, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(frame)
        top.pack(fill=tk.X)

        statut_box = ttk.LabelFrame(top, text="Statut journee (findAll)", padding=10)
        statut_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        self.tree_statuts = ttk.Treeview(statut_box, columns=("id", "nom"), show="headings", height=8)
        self.tree_statuts.heading("id", text="ID")
        self.tree_statuts.heading("nom", text="Nom")
        self.tree_statuts.pack(fill=tk.BOTH, expand=True)
        ttk.Button(statut_box, text="Charger statuts", command=self.refresh_statuts).pack(anchor="w", pady=8)

        config_box = ttk.LabelFrame(top, text="ConfigJournee", padding=10)
        config_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0))

        ttk.Label(config_box, text="Heure debut").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Label(config_box, text="Heure fin").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Label(config_box, text="Rendement (%)").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Label(config_box, text="Statut").grid(row=3, column=0, sticky="w", pady=4)

        self.entry_config_debut = ttk.Entry(config_box, width=14)
        self.entry_config_debut.insert(0, "06:00:00")
        self.entry_config_fin = ttk.Entry(config_box, width=14)
        self.entry_config_fin.insert(0, "19:00:00")
        self.entry_config_rendement = ttk.Entry(config_box, width=14)
        self.entry_config_rendement.insert(0, "40")
        self.combo_config_statut = ttk.Combobox(config_box, state="readonly", width=22)

        self.entry_config_debut.grid(row=0, column=1, padx=8)
        self.entry_config_fin.grid(row=1, column=1, padx=8)
        self.entry_config_rendement.grid(row=2, column=1, padx=8)
        self.combo_config_statut.grid(row=3, column=1, padx=8)

        ttk.Button(config_box, text="Save config", command=self.add_config).grid(row=4, column=0, pady=8)
        ttk.Button(config_box, text="Charger configs", command=self.refresh_configs).grid(row=4, column=1, sticky="w", pady=8)

        bottom = ttk.LabelFrame(frame, text="Liste ConfigJournee", padding=10)
        bottom.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree_configs = ttk.Treeview(
            bottom,
            columns=("id", "heureDebut", "heureFin", "rendement", "idStatut"),
            show="headings",
            height=8,
        )
        for col, label in zip(
            ("id", "heureDebut", "heureFin", "rendement", "idStatut"),
            ("ID", "Heure debut", "Heure fin", "Rendement", "ID Statut"),
        ):
            self.tree_configs.heading(col, text=label)
        self.tree_configs.pack(fill=tk.BOTH, expand=True)

    def _build_tab_ressource(self):
        frame = ttk.Frame(self.tab_ressource, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(frame)
        top.pack(fill=tk.X)

        res_box = ttk.LabelFrame(top, text="Ressource save/findAll", padding=10)
        res_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        ttk.Label(res_box, text="Nom").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Label(res_box, text="Puissance theorique (nullable)").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Label(res_box, text="Puissance pratique (nullable)").grid(row=2, column=0, sticky="w", pady=4)

        self.entry_res_nom = ttk.Entry(res_box, width=26)
        self.entry_res_theorique = ttk.Entry(res_box, width=12)
        self.entry_res_reelle = ttk.Entry(res_box, width=12)
        self.entry_res_nom.grid(row=0, column=1, padx=8)
        self.entry_res_theorique.grid(row=1, column=1, padx=8)
        self.entry_res_reelle.grid(row=2, column=1, padx=8)

        ttk.Button(res_box, text="Save ressource", command=self.add_ressource).grid(row=3, column=0, pady=8)
        ttk.Button(res_box, text="Charger findAll", command=self.refresh_ressources).grid(row=3, column=1, sticky="w", pady=8)

        charge_box = ttk.LabelFrame(top, text="Charge batterie", padding=10)
        charge_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0))

        ttk.Label(charge_box, text="Heure debut").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Label(charge_box, text="Heure fin").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Label(charge_box, text="Capacite (Wh)").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Label(charge_box, text="Puissance necessaire (W)").grid(row=3, column=0, sticky="w", pady=4)

        self.entry_charge_debut = ttk.Entry(charge_box, width=14)
        self.entry_charge_debut.insert(0, "10:00:00")
        self.entry_charge_fin = ttk.Entry(charge_box, width=14)
        self.entry_charge_fin.insert(0, "14:00:00")
        self.entry_charge_capacite = ttk.Entry(charge_box, width=14)
        self.entry_charge_capacite.insert(0, "240")
        self.entry_charge_puissance = ttk.Entry(charge_box, width=14)
        self.entry_charge_puissance.insert(0, "60")

        self.entry_charge_debut.grid(row=0, column=1, padx=8)
        self.entry_charge_fin.grid(row=1, column=1, padx=8)
        self.entry_charge_capacite.grid(row=2, column=1, padx=8)
        self.entry_charge_puissance.grid(row=3, column=1, padx=8)

        ttk.Button(charge_box, text="Save charge si inexistant", command=self.add_charge_if_missing).grid(row=4, column=0, pady=8)
        ttk.Button(charge_box, text="Charger charges findAll", command=self.refresh_charges).grid(row=4, column=1, sticky="w", pady=8)

        bottom = ttk.Frame(frame)
        bottom.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree_ressources = ttk.Treeview(
            bottom,
            columns=("id", "nom", "theorique", "pratique"),
            show="headings",
            height=7,
        )
        for col, label in zip(("id", "nom", "theorique", "pratique"), ("ID", "Nom", "Theorique", "Pratique")):
            self.tree_ressources.heading(col, text=label)
        self.tree_ressources.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        self.tree_charges = ttk.Treeview(
            bottom,
            columns=("id", "debut", "fin", "capacite", "puissance"),
            show="headings",
            height=7,
        )
        for col, label in zip(
            ("id", "debut", "fin", "capacite", "puissance"),
            ("ID", "Heure debut", "Heure fin", "Capacite", "Puissance"),
        ):
            self.tree_charges.heading(col, text=label)
        self.tree_charges.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0))

    def _build_tab_calcul(self):
        frame = ttk.Frame(self.tab_calcul, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)

        controls = ttk.LabelFrame(frame, text="Parametres de calcul", padding=10)
        controls.pack(fill=tk.X)

        ttk.Label(controls, text="Heure charge debut").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Label(controls, text="Heure charge fin").grid(row=0, column=2, sticky="w", pady=4)
        ttk.Label(controls, text="Marge batterie (0.50 = 50%)").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Label(controls, text="Config matin").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Label(controls, text="Config apres-midi").grid(row=2, column=2, sticky="w", pady=4)
        ttk.Label(controls, text="ID Resultat a update").grid(row=3, column=0, sticky="w", pady=4)

        self.entry_calc_charge_debut = ttk.Entry(controls, width=12)
        self.entry_calc_charge_debut.insert(0, "10:00:00")
        self.entry_calc_charge_fin = ttk.Entry(controls, width=12)
        self.entry_calc_charge_fin.insert(0, "14:00:00")
        self.entry_calc_marge = ttk.Entry(controls, width=12)
        self.entry_calc_marge.insert(0, "0.50")
        self.combo_calc_config_matin = ttk.Combobox(controls, state="readonly", width=30)
        self.combo_calc_config_apres = ttk.Combobox(controls, state="readonly", width=30)
        self.entry_calc_resultat_id = ttk.Entry(controls, width=12)

        self.entry_calc_charge_debut.grid(row=0, column=1, padx=8)
        self.entry_calc_charge_fin.grid(row=0, column=3, padx=8)
        self.entry_calc_marge.grid(row=1, column=1, padx=8)
        self.combo_calc_config_matin.grid(row=2, column=1, padx=8)
        self.combo_calc_config_apres.grid(row=2, column=3, padx=8)
        self.entry_calc_resultat_id.grid(row=3, column=1, padx=8, sticky="w")

        ttk.Button(controls, text="Analyser et calculer", command=self.run_dimensionnement).grid(row=4, column=0, pady=8)
        ttk.Button(controls, text="Recharger configs", command=self.refresh_configs).grid(row=4, column=1, sticky="w", pady=8)

        self.text_resultats = tk.Text(frame, wrap="word", height=24)
        self.text_resultats.pack(fill=tk.BOTH, expand=True, pady=10)

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
        try:
            self.connexion = Connexion(
                serve=self.entry_server.get().strip(),
                db=self.entry_db.get().strip(),
                user=self.entry_user.get().strip(),
                password=self.entry_password.get().strip(),
            )
            self.connexion.connect()
            self.sql_connection = self.connexion.connection

            if not self.sql_connection:
                raise RuntimeError("Connexion non etablie")

            materiel_repo = MaterielRepository(self.sql_connection)
            consommation_repo = ConsommationRepository(self.sql_connection)
            config_repo = ConfigJourneeRepository(self.sql_connection)
            statut_repo = StatutRepository(self.sql_connection)
            ressource_repo = RessourceRepository(self.sql_connection)
            charge_repo = ChargeBatterieRepository(self.sql_connection)
            resultat_repo = ResultatRepository(self.sql_connection)

            self.materiel_service = MaterielService(materiel_repo)
            self.consommation_service = ConsommationService(consommation_repo)
            self.config_service = ConfigJourneeService(config_repo)
            self.statut_service = StatutService(statut_repo)
            self.ressource_service = RessourceService(ressource_repo)
            self.charge_service = ChargeBatterieService(charge_repo)
            self.resultat_service = ResultatService(resultat_repo)

            self.connection_status.set("Connecte")
            self.refresh_all()
            messagebox.showinfo("Connexion", "Connexion reussie.")
        except Exception as exc:
            self.connection_status.set("Erreur de connexion")
            messagebox.showerror("Connexion", f"Echec connexion: {exc}")

    def refresh_all(self):
        if not self._ensure_connected():
            return
        self.refresh_materiels()
        self.refresh_statuts()
        self.refresh_configs()
        self.refresh_consommations()
        self.refresh_ressources()
        self.refresh_charges()

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
        except ValueError:
            messagebox.showwarning("Ressource", "Valeurs puissance invalides")
            return

        res = Ressource(None, nom, p_theo, p_pratique)
        ok = self.ressource_service.save(res)
        if ok:
            self.refresh_ressources()
            messagebox.showinfo("Ressource", "Ressource enregistree")
        else:
            messagebox.showerror("Ressource", "Save ressource echoue")

    def refresh_ressources(self):
        if not self._ensure_connected():
            return
        self._clear_tree(self.tree_ressources)
        rows = self.ressource_service.findAll() or []
        for row in rows:
            self.tree_ressources.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))

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

    def _upsert_ressource(self, nom, puissance_theorique, puissance_pratique):
        matches = self.ressource_service.findByNom(nom) or []
        chosen = None
        for row in matches:
            if row[1].strip().lower() == nom.strip().lower():
                chosen = row
                break

        if chosen:
            self.ressource_service.update(chosen[0], nom=nom, puissanceTheorique=puissance_theorique, puissanceReelle=puissance_pratique)
            return chosen[0]

        self.ressource_service.save(Ressource(None, nom, puissance_theorique, puissance_pratique))
        matches = self.ressource_service.findByNom(nom) or []
        for row in matches:
            if row[1].strip().lower() == nom.strip().lower():
                return row[0]
        return None

    def run_dimensionnement(self):
        if not self._ensure_connected():
            return

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
        
        # 5. Panneau théorique = (pic + charge) / rendement
        selected_matin = self.combo_calc_config_matin.get().strip()
        config_matin_id = self.config_label_to_id.get(selected_matin)
        
        rendement = 0.40  # Default 40%
        if config_matin_id:
            cfg = self._get_config_by_id(config_matin_id)
            if cfg:
                rendement = float(cfg.rendement) / 100.0
        
        # Panneau pratique = pic + charge
        panneau_pratique = p_max + p_charge
        
        # Panneau théorique = pratique / rendement
        panneau_theorique = panneau_pratique / rendement if rendement > 0 else 0.0
        
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
        
        # Ressources
        id_res_panneau = self._upsert_ressource(
            "Panneau solaire scolaire",
            panneau_theorique,
            panneau_pratique,
        )
        id_res_batterie = self._upsert_ressource(
            "Batterie scolaire",
            batterie_reelle,
            batterie_nuit,
        )
        
        self.refresh_ressources()
        self.refresh_charges()
        
        # Affichage simple
        lines = [
            "=== CALCUL SOLAIRE (MÉTHODE NUIT SEULEMENT) ===",
            "",
            f"Batterie (nuit 19:00→06:00): {batterie_nuit:.2f} Wh",
            f"Batterie réelle (×1.5): {batterie_reelle:.2f} Wh",
            "",
            f"Puissance recharge batterie (÷12h): {p_charge:.2f} W",
            "",
            f"Besoin matin (06:00→17:00): {besoin_matin:.2f} W",
            f"Besoin après-midi (17:00→19:00): {besoin_midi:.2f} W",
            f"Pic instantané: {p_max:.2f} W",
            "",
            f"Panneau solaire pratique: {panneau_pratique:.2f} W",
            f"Panneau solaire théorique (÷{rendement*100:.0f}%): {panneau_theorique:.2f} W",
        ]
        
        self.text_resultats.delete("1.0", tk.END)
        self.text_resultats.insert(tk.END, "\n".join(lines))


def run():
    root = tk.Tk()
    SolaireGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run()
