import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
from pathlib import Path

# Ajouter le chemin parent pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from Services.MaterielService import MaterielService
from Services.ConsommationService import ConsommationService
from Models.Materiel import Materiel
from Models.Consommation import Consommation


class MaterielInterface:
    """Interface tkinter pour gérer les matériels et leurs consommations"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Matériels et Consommations")
        self.root.geometry("900x700")
        
        # Services
        self.materiel_service = MaterielService()
        self.consommation_service = ConsommationService()
        
        # Variables
        self.selected_materiel_id = None
        self.materiels_data = []
        
        # Interface setup
        self.setup_ui()
        self.charger_materiels()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ============ Section Ajout Matériel ============
        materiel_frame = ttk.LabelFrame(main_frame, text="Ajouter un Matériel", padding="10")
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
        
        # Bouton Ajouter
        btn_ajouter = ttk.Button(materiel_frame, text="Ajouter Matériel", command=self.ajouter_materiel)
        btn_ajouter.grid(row=3, column=0, columnspan=2, pady=10)
        
        # ============ Section Liste des Matériels ============
        list_frame = ttk.LabelFrame(main_frame, text="Liste des Matériels", padding="10")
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Treeview pour afficher les matériels
        columns = ("ID", "Nom", "Type", "Puissance (W)")
        self.tree = ttk.Treeview(list_frame, columns=columns, height=15)
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.W, width=50)
        self.tree.column("Nom", anchor=tk.W, width=250)
        self.tree.column("Type", anchor=tk.W, width=200)
        self.tree.column("Puissance (W)", anchor=tk.CENTER, width=150)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Nom", text="Nom", anchor=tk.W)
        self.tree.heading("Type", text="Type", anchor=tk.W)
        self.tree.heading("Puissance (W)", text="Puissance (W)", anchor=tk.CENTER)
        
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
        consommation_frame = ttk.LabelFrame(main_frame, text="Résumé", padding="10")
        consommation_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.label_total_puissance = ttk.Label(consommation_frame, text="Puissance totale: 0 W", font=("Arial", 12, "bold"))
        self.label_total_puissance.grid(row=0, column=0, sticky=tk.W, padx=5)
        
    def charger_materiels(self):
        """Charger et afficher tous les matériels"""
        try:
            # Nettoyer l'affichage
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Récupérer les matériels
            self.materiels_data = self.materiel_service.get_all()
            
            # Ajouter à l'affichage
            total_puissance = 0
            for materiel in self.materiels_data:
                puissance = materiel.get('puissance', 0)
                self.tree.insert("", "end", values=(
                    materiel.get('id', ''),
                    materiel.get('nom', ''),
                    materiel.get('type', ''),
                    f"{puissance} W"
                ))
                total_puissance += puissance
            
            # Mettre à jour le résumé
            self.label_total_puissance.config(text=f"Puissance totale: {total_puissance} W")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def ajouter_materiel(self):
        """Ajouter un nouveau matériel"""
        nom = self.entry_nom.get().strip()
        type_materiel = self.entry_type.get().strip()
        puissance_str = self.entry_puissance.get().strip()
        
        # Validation
        if not nom or not type_materiel or not puissance_str:
            messagebox.showwarning("Validation", "Tous les champs sont obligatoires!")
            return
        
        try:
            puissance = float(puissance_str)
            
            # Créer le matériel
            nouveau_materiel = Materiel(
                id=None,
                nom=nom,
                type=type_materiel,
                puissance=puissance
            )
            
            # Sauvegarder
            self.materiel_service.create(nouveau_materiel)
            
            # Nettoyer les champs
            self.entry_nom.delete(0, tk.END)
            self.entry_type.delete(0, tk.END)
            self.entry_puissance.delete(0, tk.END)
            
            # Rafraîchir l'affichage
            self.charger_materiels()
            messagebox.showinfo("Succès", "Matériel ajouté avec succès!")
            
        except ValueError:
            messagebox.showerror("Erreur", "La puissance doit être un nombre!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def on_materiel_select(self, event):
        """Gérer la sélection d'un matériel"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            self.selected_materiel_id = self.tree.item(item, "values")[0]
    
    def modifier_materiel(self):
        """Modifier le matériel sélectionné"""
        if not self.selected_materiel_id:
            messagebox.showwarning("Attention", "Veuillez sélectionner un matériel!")
            return
        
        # Récupérer le matériel
        materiel = next((m for m in self.materiels_data if m.get('id') == int(self.selected_materiel_id)), None)
        if not materiel:
            messagebox.showerror("Erreur", "Matériel non trouvé!")
            return
        
        # Fenêtre de modification
        dialog = tk.Toplevel(self.root)
        dialog.title("Modifier Matériel")
        dialog.geometry("400x250")
        
        ttk.Label(dialog, text="Nom:").grid(row=0, column=0, padx=10, pady=5)
        entry_nom = ttk.Entry(dialog, width=30)
        entry_nom.insert(0, materiel.get('nom', ''))
        entry_nom.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Type:").grid(row=1, column=0, padx=10, pady=5)
        entry_type = ttk.Entry(dialog, width=30)
        entry_type.insert(0, materiel.get('type', ''))
        entry_type.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Puissance (W):").grid(row=2, column=0, padx=10, pady=5)
        entry_puissance = ttk.Entry(dialog, width=30)
        entry_puissance.insert(0, str(materiel.get('puissance', '')))
        entry_puissance.grid(row=2, column=1, padx=10, pady=5)
        
        def sauvegarder():
            try:
                materiel_modifie = Materiel(
                    id=int(self.selected_materiel_id),
                    nom=entry_nom.get().strip(),
                    type=entry_type.get().strip(),
                    puissance=float(entry_puissance.get().strip())
                )
                self.materiel_service.update(materiel_modifie)
                dialog.destroy()
                self.charger_materiels()
                messagebox.showinfo("Succès", "Matériel modifié avec succès!")
            except ValueError:
                messagebox.showerror("Erreur", "La puissance doit être un nombre!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")
        
        ttk.Button(dialog, text="Sauvegarder", command=sauvegarder).grid(row=3, column=0, columnspan=2, pady=10)
    
    def supprimer_materiel(self):
        """Supprimer le matériel sélectionné"""
        if not self.selected_materiel_id:
            messagebox.showwarning("Attention", "Veuillez sélectionner un matériel!")
            return
        
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce matériel?"):
            try:
                self.materiel_service.delete(int(self.selected_materiel_id))
                self.charger_materiels()
                messagebox.showinfo("Succès", "Matériel supprimé avec succès!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")


def main():
    """Lancer l'application"""
    root = tk.Tk()
    app = MaterielInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
