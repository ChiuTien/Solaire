import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le chemin parent pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from Services.MaterielService import MaterielService
from Services.ConsommationService import ConsommationService
from Models.Materiel import Materiel
from Models.Consommation import Consommation


class MaterielInterface:
    """Interface tkinter pour gérer des enregistrements fusionnés Matériel + Consommation."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion Fusionnee Materiel + Consommation")
        self.root.geometry("1200x720")
        
        # Services
        self.materiel_service = MaterielService()
        self.consommation_service = ConsommationService()
        
        # Variables
        self.selected_materiel_id = None
        self.selected_consommation_id = None
        self.rows_data = []
        
        # Interface setup
        self.setup_ui()
        self.charger_materiels()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ============ Section Ajout Fusion ============
        materiel_frame = ttk.LabelFrame(main_frame, text="Ajouter un Materiel (fusion Materiel + Consommation)", padding="10")
        materiel_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Nom du matériel
        ttk.Label(materiel_frame, text="Nom du matériel:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.entry_nom = ttk.Entry(materiel_frame, width=30)
        self.entry_nom.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Type du matériel
        ttk.Label(materiel_frame, text="Type:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.entry_type = ttk.Entry(materiel_frame, width=30)
        self.entry_type.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Puissance (consommation)
        ttk.Label(materiel_frame, text="Puissance (W):").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.entry_puissance = ttk.Entry(materiel_frame, width=30)
        self.entry_puissance.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(materiel_frame, text="Heure debut (HH:MM):").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.entry_heure_debut = ttk.Entry(materiel_frame, width=20)
        self.entry_heure_debut.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5)
        self.entry_heure_debut.insert(0, "08:00")

        ttk.Label(materiel_frame, text="Heure fin (HH:MM):").grid(row=1, column=2, sticky=tk.W, padx=5)
        self.entry_heure_fin = ttk.Entry(materiel_frame, width=20)
        self.entry_heure_fin.grid(row=1, column=3, sticky=(tk.W, tk.E), padx=5)
        self.entry_heure_fin.insert(0, "18:00")
        
        # Bouton Ajouter
        btn_ajouter = ttk.Button(materiel_frame, text="Ajouter Entree Fusionnee", command=self.ajouter_materiel)
        btn_ajouter.grid(row=3, column=0, columnspan=4, pady=10)
        
        # ============ Section Liste des Matériels ============
        list_frame = ttk.LabelFrame(main_frame, text="Liste fusionnee", padding="10")
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Treeview pour afficher les matériels
        columns = ("ID Materiel", "ID Consommation", "Nom", "Type", "Puissance (W)", "Heure debut", "Heure fin")
        self.tree = ttk.Treeview(list_frame, columns=columns, height=15)
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID Materiel", anchor=tk.W, width=95)
        self.tree.column("ID Consommation", anchor=tk.W, width=120)
        self.tree.column("Nom", anchor=tk.W, width=220)
        self.tree.column("Type", anchor=tk.W, width=160)
        self.tree.column("Puissance (W)", anchor=tk.CENTER, width=120)
        self.tree.column("Heure debut", anchor=tk.CENTER, width=120)
        self.tree.column("Heure fin", anchor=tk.CENTER, width=120)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID Materiel", text="ID Materiel", anchor=tk.W)
        self.tree.heading("ID Consommation", text="ID Consommation", anchor=tk.W)
        self.tree.heading("Nom", text="Nom", anchor=tk.W)
        self.tree.heading("Type", text="Type", anchor=tk.W)
        self.tree.heading("Puissance (W)", text="Puissance (W)", anchor=tk.CENTER)
        self.tree.heading("Heure debut", text="Heure debut", anchor=tk.CENTER)
        self.tree.heading("Heure fin", text="Heure fin", anchor=tk.CENTER)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.tree.bind("<<TreeviewSelect>>", self.on_materiel_select)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscroll=scrollbar.set)
        
        # ============ Section Actions ============
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        btn_modifier = ttk.Button(action_frame, text="Modifier", command=self.modifier_materiel)
        btn_modifier.grid(row=0, column=0, padx=5)
        
        btn_supprimer = ttk.Button(action_frame, text="Supprimer", command=self.supprimer_materiel)
        btn_supprimer.grid(row=0, column=1, padx=5)
        
        btn_rafraichir = ttk.Button(action_frame, text="Rafraîchir", command=self.charger_materiels)
        btn_rafraichir.grid(row=0, column=2, padx=5)
        
        # ============ Section Consommation Total ============
        consommation_frame = ttk.LabelFrame(main_frame, text="Resume", padding="10")
        consommation_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.label_total_puissance = ttk.Label(consommation_frame, text="Puissance totale: 0 W", font=("Arial", 12, "bold"))
        self.label_total_puissance.grid(row=0, column=0, sticky=tk.W, padx=5)

        self.label_total_entrees = ttk.Label(consommation_frame, text="Nombre d'entrees: 0", font=("Arial", 11))
        self.label_total_entrees.grid(row=0, column=1, sticky=tk.W, padx=25)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

    def _format_heure(self, valeur):
        texte = (valeur or "").strip()
        if not texte:
            raise ValueError("Les heures sont obligatoires")
        if len(texte) == 5:
            datetime.strptime(texte, "%H:%M")
            return f"{texte}:00"
        datetime.strptime(texte, "%H:%M:%S")
        return texte

    def _clear_form(self):
        self.entry_nom.delete(0, tk.END)
        self.entry_type.delete(0, tk.END)
        self.entry_puissance.delete(0, tk.END)
        self.entry_heure_debut.delete(0, tk.END)
        self.entry_heure_fin.delete(0, tk.END)
        self.entry_heure_debut.insert(0, "08:00")
        self.entry_heure_fin.insert(0, "18:00")

    def _build_fusion_rows(self):
        materiels = self.materiel_service.get_all() or []
        consommations = self.consommation_service.get_all() or []

        mat_by_id = {m.get("id"): m for m in materiels if m.get("id") is not None}
        rows = []
        total_puissance = 0.0

        for consommation in consommations:
            id_materiel = consommation.get("idMateriel")
            materiel = mat_by_id.get(id_materiel, {})
            puissance = float(consommation.get("puissance") or materiel.get("puissance") or 0)
            total_puissance += puissance

            rows.append({
                "materiel_id": id_materiel,
                "consommation_id": consommation.get("id"),
                "nom": materiel.get("nom", ""),
                "type": materiel.get("type", ""),
                "puissance": puissance,
                "heure_debut": consommation.get("heureDebut", ""),
                "heure_fin": consommation.get("heureFin", ""),
            })

        return rows, total_puissance
        
    def charger_materiels(self):
        """Charger et afficher la fusion Materiel + Consommation."""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            self.rows_data, total_puissance = self._build_fusion_rows()

            for row in self.rows_data:
                self.tree.insert("", "end", values=(
                    row.get("materiel_id", ""),
                    row.get("consommation_id", ""),
                    row.get("nom", ""),
                    row.get("type", ""),
                    f"{row.get('puissance', 0)} W",
                    row.get("heure_debut", ""),
                    row.get("heure_fin", ""),
                ))

            self.label_total_puissance.config(text=f"Puissance totale: {total_puissance} W")
            self.label_total_entrees.config(text=f"Nombre d'entrees: {len(self.rows_data)}")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def ajouter_materiel(self):
        """Ajouter une entree fusionnee: Materiel + Consommation."""
        nom = self.entry_nom.get().strip()
        type_materiel = self.entry_type.get().strip()
        puissance_str = self.entry_puissance.get().strip()
        heure_debut_str = self.entry_heure_debut.get().strip()
        heure_fin_str = self.entry_heure_fin.get().strip()
        
        # Validation
        if not nom or not type_materiel or not puissance_str or not heure_debut_str or not heure_fin_str:
            messagebox.showwarning("Validation", "Tous les champs sont obligatoires!")
            return

        try:
            puissance = float(puissance_str)
            heure_debut = self._format_heure(heure_debut_str)
            heure_fin = self._format_heure(heure_fin_str)

            anciens_ids = {m.get("id") for m in (self.materiel_service.get_all() or []) if m.get("id") is not None}

            nouveau_materiel = Materiel(
                id=None,
                nom=nom,
                type=type_materiel,
                puissance=puissance
            )

            self.materiel_service.create(nouveau_materiel)

            nouveaux_materiels = self.materiel_service.get_all() or []
            nouveaux_ids = [m.get("id") for m in nouveaux_materiels if m.get("id") is not None and m.get("id") not in anciens_ids]
            id_materiel = nouveau_materiel.id if nouveau_materiel.id is not None else (max(nouveaux_ids) if nouveaux_ids else None)

            if id_materiel is None:
                raise ValueError("Impossible de determiner l'ID du materiel apres insertion")

            nouvelle_consommation = Consommation(
                id=None,
                idMateriel=id_materiel,
                puissance=puissance,
                heureDebut=heure_debut,
                heureFin=heure_fin,
            )
            self.consommation_service.create(nouvelle_consommation)

            self._clear_form()
            self.charger_materiels()
            messagebox.showinfo("Succes", "Entree fusionnee ajoutee avec succes")

        except ValueError:
            messagebox.showerror("Erreur", "Puissance ou heures invalides (format heure: HH:MM ou HH:MM:SS)")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def on_materiel_select(self, event):
        """Gerer la selection d'une ligne fusionnee."""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            valeurs = self.tree.item(item, "values")
            self.selected_materiel_id = int(valeurs[0]) if valeurs and valeurs[0] else None
            self.selected_consommation_id = int(valeurs[1]) if len(valeurs) > 1 and valeurs[1] else None
    
    def modifier_materiel(self):
        """Modifier la ligne fusionnee selectionnee."""
        if not self.selected_materiel_id or not self.selected_consommation_id:
            messagebox.showwarning("Attention", "Veuillez selectionner une entree!")
            return

        row = next(
            (
                r
                for r in self.rows_data
                if r.get("materiel_id") == self.selected_materiel_id
                and r.get("consommation_id") == self.selected_consommation_id
            ),
            None,
        )
        if not row:
            messagebox.showerror("Erreur", "Entree non trouvee!")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Modifier entree fusionnee")
        dialog.geometry("520x300")

        ttk.Label(dialog, text="Nom:").grid(row=0, column=0, padx=10, pady=5)
        entry_nom = ttk.Entry(dialog, width=30)
        entry_nom.insert(0, row.get("nom", ""))
        entry_nom.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Type:").grid(row=1, column=0, padx=10, pady=5)
        entry_type = ttk.Entry(dialog, width=30)
        entry_type.insert(0, row.get("type", ""))
        entry_type.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Puissance (W):").grid(row=2, column=0, padx=10, pady=5)
        entry_puissance = ttk.Entry(dialog, width=30)
        entry_puissance.insert(0, str(row.get("puissance", "")))
        entry_puissance.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Heure debut (HH:MM):").grid(row=0, column=2, padx=10, pady=5)
        entry_heure_debut = ttk.Entry(dialog, width=20)
        entry_heure_debut.insert(0, str(row.get("heure_debut", ""))[:5])
        entry_heure_debut.grid(row=0, column=3, padx=10, pady=5)

        ttk.Label(dialog, text="Heure fin (HH:MM):").grid(row=1, column=2, padx=10, pady=5)
        entry_heure_fin = ttk.Entry(dialog, width=20)
        entry_heure_fin.insert(0, str(row.get("heure_fin", ""))[:5])
        entry_heure_fin.grid(row=1, column=3, padx=10, pady=5)

        def sauvegarder():
            try:
                puissance = float(entry_puissance.get().strip())
                heure_debut = self._format_heure(entry_heure_debut.get().strip())
                heure_fin = self._format_heure(entry_heure_fin.get().strip())

                materiel_modifie = Materiel(
                    id=self.selected_materiel_id,
                    nom=entry_nom.get().strip(),
                    type=entry_type.get().strip(),
                    puissance=puissance,
                )
                self.materiel_service.update(materiel_modifie)
                self.consommation_service.update(
                    self.selected_consommation_id,
                    idMateriel=self.selected_materiel_id,
                    puissance=puissance,
                    heureDebut=heure_debut,
                    heureFin=heure_fin,
                )
                dialog.destroy()
                self.charger_materiels()
                messagebox.showinfo("Succes", "Entree fusionnee modifiee avec succes")
            except ValueError:
                messagebox.showerror("Erreur", "Puissance ou heures invalides (format heure: HH:MM ou HH:MM:SS)")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")

        ttk.Button(dialog, text="Sauvegarder", command=sauvegarder).grid(row=3, column=0, columnspan=2, pady=10)
    
    def supprimer_materiel(self):
        """Supprimer une entree fusionnee (consommation + eventuel materiel orphelin)."""
        if not self.selected_materiel_id or not self.selected_consommation_id:
            messagebox.showwarning("Attention", "Veuillez selectionner une entree!")
            return

        if messagebox.askyesno("Confirmation", "Supprimer cette entree fusionnee ?"):
            try:
                self.consommation_service.delete(self.selected_consommation_id)

                restantes = self.consommation_service.findByMateriel(self.selected_materiel_id) or []
                if len(restantes) == 0:
                    self.materiel_service.delete(self.selected_materiel_id)

                self.selected_materiel_id = None
                self.selected_consommation_id = None
                self.charger_materiels()
                messagebox.showinfo("Succes", "Entree fusionnee supprimee avec succes")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")


def main():
    """Lancer l'application"""
    root = tk.Tk()
    app = MaterielInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
