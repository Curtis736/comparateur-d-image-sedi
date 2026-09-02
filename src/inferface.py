import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
import VerifPdf
import VerifPdfRoutine
import Log
import sys
import subprocess

class InterfaceVerificationPDF:
    def __init__(self, root):
        self.root = root
        self.root.title("Vérificateur de PDFs - Contrôle SN et Programmes")
        self.root.geometry("1200x800")
        self.root.configure(bg="#000000")
        
        # Variables
        self.selected_folder = None
        self.program_name = "Elio_Muxis_V1 / Dichroique_940-1310"
        self.is_verifying = False
        self.verification_results = []
        self.pdf_paths = []
        
        # Initialiser le système de logs
        Log.Init()
        
        self.setup_ui()
        self.setup_log_callbacks()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Style moderne
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuration des couleurs et styles
        style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'), foreground="#000000")
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#ecf0f1')
        style.configure('Custom.TButton', font=('Segoe UI', 10), padding=8)
        style.configure('Status.TLabel', font=('Segoe UI', 10), foreground='#ecf0f1')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Titre principal
        title_label = ttk.Label(main_frame, text="📋 Vérificateur de PDFs", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de configuration
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        config_frame.columnconfigure(1, weight=1)
        
        # Sélection du dossier
        ttk.Label(config_frame, text="📁 Dossier à vérifier:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        
        folder_frame = ttk.Frame(config_frame)
        folder_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        folder_frame.columnconfigure(0, weight=1)
        
        self.folder_var = tk.StringVar()
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, state='readonly')
        self.folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(folder_frame, text="📂 Parcourir", command=self.select_folder, 
                  style='Custom.TButton').grid(row=0, column=1)
        
        # Nom du programme
        ttk.Label(config_frame, text="🔧 Programme attendu:", style='Header.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.program_var = tk.StringVar(value="Elio_Muxis_V1 / Dichroique_940-1310")
        program_entry = ttk.Entry(config_frame, textvariable=self.program_var, width=30, state='readonly')
        program_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Frame des contrôles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        # Boutons de contrôle
        ttk.Button(controls_frame, text="🔍 Démarrer la vérification", 
                  command=self.start_verification, style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="⏹️ Arrêter", 
                  command=self.stop_verification, style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="🗑️ Effacer les logs", 
                  command=self.clear_logs, style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="💾 Sauvegarder rapport", 
                  command=self.save_report, style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        
        # Frame des résultats
        results_frame = ttk.LabelFrame(main_frame, text="📊 Résultats de la vérification", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Notebook pour organiser les résultats
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Onglet Logs en temps réel
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📝 Logs en temps réel")
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(0, weight=1)
        
        # Zone de texte pour les logs
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=15, width=80, 
                                                 font=('Consolas', 10), bg='#2c3e50', fg='#ecf0f1')
        self.logs_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Onglet Résumé
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="📋 Résumé")
        summary_frame.columnconfigure(0, weight=1)
        summary_frame.rowconfigure(0, weight=1)
        
        # Zone de texte pour le résumé
        self.summary_text = scrolledtext.ScrolledText(summary_frame, height=15, width=80,
                                                    font=('Consolas', 10), bg='#2c3e50', fg='#ecf0f1')
        self.summary_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Onglet Fichiers
        files_frame = ttk.Frame(self.notebook)
        self.notebook.add(files_frame, text="📂 Fichiers")
        files_frame.columnconfigure(0, weight=1)
        files_frame.rowconfigure(0, weight=1)
        
        self.files_listbox = tk.Listbox(files_frame, height=15)
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.files_listbox.bind('<Double-Button-1>', self.on_open_selected_pdf)
        
        open_btn = ttk.Button(files_frame, text="🖺 Ouvrir le PDF", command=self.open_selected_pdf, style='Custom.TButton')
        open_btn.grid(row=1, column=0, sticky=tk.W, pady=5)
         
        # Frame de statut
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(1, weight=1)
        
        # Barre de progression
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Label de statut
        self.status_label = ttk.Label(status_frame, text="Prêt", style='Status.TLabel')
        self.status_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Compteurs
        self.counters_label = ttk.Label(status_frame, text="Fichiers: 0 | Erreurs: 0 | Succès: 0", 
                                       style='Status.TLabel')
        self.counters_label.grid(row=1, column=1, sticky=tk.E, pady=5)
        
        # Message initial
        self.logs_text.insert(tk.END, "🚀 Vérificateur de PDFs initialisé\n")
        self.logs_text.insert(tk.END, "Sélectionnez un dossier pour commencer.\n")
        self.logs_text.insert(tk.END, "Programmes: Elio_Muxis_V1 (dossier standard) ou Dichroique_940-1310 (dossier finissant par DICRO)\n\n")
        self.logs_text.see(tk.END)
        
    def setup_log_callbacks(self):
        """Configure les callbacks pour les logs"""
        Log.AddCallback(Log.Lvl.MSG, self.add_log_message)
        Log.AddCallback(Log.Lvl.WARN, self.add_log_warning)
        Log.AddCallback(Log.Lvl.ERR, self.add_log_error)
        Log.AddCallback(Log.Lvl.VERB, self.add_log_verbose)
        
    def _update_expected_program_display(self):
        """Met à jour l'affichage du profil attendu selon le nom du dossier."""
        if self.selected_folder:
            expected = VerifPdfRoutine._get_expected_program_for_folder(self.selected_folder)
            self.program_name = expected
            self.program_var.set(expected)
        else:
            self.program_name = "Elio_Muxis_V1 / Dichroique_940-1310"
            self.program_var.set("Elio_Muxis_V1 / Dichroique_940-1310")

    def select_folder(self):
        """Sélectionne un dossier à vérifier"""
        folder = filedialog.askdirectory(title="Sélectionner le dossier contenant les PDFs")
        if folder:
            self.selected_folder = folder
            self.folder_var.set(folder)
            self._update_expected_program_display()
            Log.Message(f"Dossier sélectionné: {folder}")
            if VerifPdfRoutine._is_dicro_folder(folder):
                Log.Message(f"Profil attendu (dossier DICRO): {VerifPdfRoutine.DICRO_PROGRAM}")
            else:
                Log.Message(f"Profil attendu: {VerifPdfRoutine.DEFAULT_PROGRAM}")
            
            # Compter les PDFs dans le dossier
            pdf_count = 0
            try:
                pdf_files = [file for file in os.listdir(folder) if file.lower().endswith('.pdf')]
                pdf_count = len(pdf_files)
                Log.Message(f"Nombre de fichiers PDF trouvés: {pdf_count}")
                # Remplir l'onglet Fichiers
                self.pdf_paths = [os.path.join(folder, f) for f in pdf_files]
                self.files_listbox.delete(0, tk.END)
                for f in pdf_files:
                    self.files_listbox.insert(tk.END, f)
            except Exception as e:
                Log.Error(f"Erreur lors du scan du dossier: {e}")
                
    def start_verification(self):
        """Démarre la vérification dans un thread séparé"""
        if not self.selected_folder:
            messagebox.showwarning("Attention", "Veuillez sélectionner un dossier.")
            return
            
        if self.is_verifying:
            messagebox.showinfo("Info", "Une vérification est déjà en cours.")
            return
            
        # Programme figé dans l'interface
        self.program_name = self.program_var.get().strip()
            
        # Démarrer la vérification dans un thread séparé
        self.is_verifying = True
        self.verification_thread = threading.Thread(target=self.run_verification)
        self.verification_thread.daemon = True
        self.verification_thread.start()
        
        # Mettre à jour l'interface
        self.status_label.config(text="Vérification en cours...")
        self.progress_var.set(0)
        
    def run_verification(self):
        """Exécute la vérification"""
        try:
            Log.Message(f"Début de la vérification du dossier: {self.selected_folder}")
            expected = VerifPdfRoutine._get_expected_program_for_folder(self.selected_folder)
            Log.Message(f"Profil attendu pour ce dossier: {expected}")
            
            # Compter les fichiers PDF
            pdf_files = [f for f in os.listdir(self.selected_folder) if f.lower().endswith('.pdf')]
            total_files = len(pdf_files)
            
            if total_files == 0:
                Log.Warning("Aucun fichier PDF trouvé dans le dossier sélectionné.")
                self.root.after(0, self.verification_completed, False)
                return
                
            Log.Message(f"Nombre de fichiers PDF à vérifier: {total_files}")
            
            # Lancer la vérification
            success = VerifPdfRoutine.VerifyFolder(self.selected_folder, None)
            
            # Mettre à jour la progression
            self.root.after(0, lambda: self.progress_var.set(100))
            
            # Afficher le résultat final
            if success:
                Log.Message("✅ Vérification terminée avec succès - Aucune erreur détectée")
            else:
                Log.Warning("⚠️ Vérification terminée avec des erreurs")
                
            self.root.after(0, self.verification_completed, success)
            
        except Exception as e:
            Log.Error(f"Erreur lors de la vérification: {e}")
            self.root.after(0, self.verification_completed, False)

    def verification_completed(self, success):
        """Appelée quand la vérification est terminée"""
        self.is_verifying = False
        if success:
            self.status_label.config(text="Vérification terminée avec succès")
        else:
            self.status_label.config(text="Vérification terminée avec des erreurs")
            
        # Créer le résumé
        self.create_summary()
        
    def stop_verification(self):
        """Arrête la vérification en cours"""
        if self.is_verifying:
            self.is_verifying = False
            self.status_label.config(text="Vérification arrêtée")
            Log.Message("Vérification arrêtée par l'utilisateur")
        
    def clear_logs(self):
        """Efface tous les logs"""
        self.logs_text.delete(1.0, tk.END)
        self.summary_text.delete(1.0, tk.END)
        self.logs_text.insert(tk.END, "Logs effacés.\n")
        self.logs_text.see(tk.END)
        
    def create_summary(self):
        """Crée un résumé de la vérification"""
        self.summary_text.delete(1.0, tk.END)
        
        # Analyser les logs pour créer le résumé
        log_content = self.logs_text.get(1.0, tk.END)
        
        # Compter les différents types de messages
        error_count = log_content.count("[ERROR]")
        warning_count = log_content.count("[WARN]")
        message_count = log_content.count("[MSG]")
        
        # Créer le résumé
        summary = "📊 RÉSUMÉ DE LA VÉRIFICATION\n"
        summary += "=" * 50 + "\n\n"
        
        if self.selected_folder:
            summary += f"📁 Dossier vérifié: {self.selected_folder}\n"
        if self.program_name:
            summary += f"🔧 Programme attendu: {self.program_name}\n"
            
        summary += f"\n📈 STATISTIQUES:\n"
        summary += f"• Messages d'information: {message_count}\n"
        summary += f"• Avertissements: {warning_count}\n"
        summary += f"• Erreurs: {error_count}\n"
        
        # Analyser les erreurs spécifiques
        if error_count > 0:
            summary += f"\n❌ ERREURS DÉTECTÉES:\n"
            lines = log_content.split('\n')
            for line in lines:
                if "[ERROR]" in line:
                    summary += f"• {line.strip()}\n"
                    
        if warning_count > 0:
            summary += f"\n⚠️ AVERTISSEMENTS:\n"
            lines = log_content.split('\n')
            for line in lines:
                if "[WARN]" in line:
                    summary += f"• {line.strip()}\n"
                    
        # Recommandations
        summary += f"\n💡 RECOMMANDATIONS:\n"
        if error_count == 0:
            summary += "• Tous les fichiers PDF sont conformes aux exigences\n"
        else:
            summary += "• Vérifiez les fichiers mentionnés dans les erreurs\n"
            summary += "• Assurez-vous que les noms de fichiers contiennent les bons SN\n"
            summary += "• Vérifiez que les PDFs contiennent les informations attendues\n"
            
        self.summary_text.insert(tk.END, summary)
        self.summary_text.see(tk.END)
        
    def save_report(self):
        """Sauvegarde le rapport de vérification"""
        if not self.selected_folder:
            messagebox.showwarning("Attention", "Aucun rapport à sauvegarder.")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Sauvegarder le rapport",
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("RAPPORT DE VÉRIFICATION PDF\n")
                    f.write("=" * 50 + "\n\n")
                    
                    # Informations générales
                    f.write(f"Dossier vérifié: {self.selected_folder}\n")
                    f.write(f"Programme attendu: {self.program_name}\n")
                    f.write(f"Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    # Logs complets
                    f.write("LOGS COMPLETS:\n")
                    f.write("-" * 30 + "\n")
                    f.write(self.logs_text.get(1.0, tk.END))
                    f.write("\n\n")
                    
                    # Résumé
                    f.write("RÉSUMÉ:\n")
                    f.write("-" * 30 + "\n")
                    f.write(self.summary_text.get(1.0, tk.END))
                    
                messagebox.showinfo("Succès", f"Rapport sauvegardé dans {file_path}")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder: {str(e)}")
                
    def add_log_message(self, message):
        """Ajoute un message de log"""
        self.root.after(0, self._add_log, message, "MSG")
        
    def add_log_warning(self, message):
        """Ajoute un avertissement de log"""
        self.root.after(0, self._add_log, message, "WARN")
        
    def add_log_error(self, message):
        """Ajoute une erreur de log"""
        self.root.after(0, self._add_log, message, "ERROR")
        
    def add_log_verbose(self, message):
        """Ajoute un message verbose de log"""
        self.root.after(0, self._add_log, message, "VERB")
        
    def _add_log(self, message, level):
        """Ajoute un message de log dans l'interface"""
        # Activer l'édition
        self.logs_text.config(state=tk.NORMAL)
        
        # Ajouter le message avec couleur selon le niveau
        if level == "ERROR":
            self.logs_text.insert(tk.END, message, "error")
        elif level == "WARN":
            self.logs_text.insert(tk.END, message, "warning")
        elif level == "MSG":
            self.logs_text.insert(tk.END, message, "MSG")
        elif level == "VERB":
            self.logs_text.insert(tk.END, message, "verbose")
        
        # Ajout d'un retour à la ligne
        self.logs_text.insert(tk.END, "\n")
        
        # Garder le scroll en bas
        self.logs_text.see(tk.END)
        
        # Désactiver l'édition
        self.logs_text.config(state=tk.DISABLED)
        
    def on_open_selected_pdf(self, event=None):
        """Ouvre le PDF sélectionné depuis l'onglet Fichiers"""
        selection = self.files_listbox.curselection()
        if selection:
            index = selection[0]
            file_path = self.pdf_paths[index]
            self.open_pdf(file_path)
        
    def open_selected_pdf(self):
        """Ouvre le PDF sélectionné (bouton explicit)"""
        selection = self.files_listbox.curselection()
        if selection:
            index = selection[0]
            file_path = self.pdf_paths[index]
            self.open_pdf(file_path)
        
    def open_pdf(self, file_path):
        """Ouvre un fichier PDF dans le lecteur système par défaut"""
        try:
            if sys.platform.startswith('win'):
                os.startfile(file_path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', file_path])
            else:
                subprocess.run(['xdg-open', file_path])
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier: {str(e)}")

def main():
    """Fonction principale pour lancer l'application"""
    root = tk.Tk()
    app = InterfaceVerificationPDF(root)
    
    # Configuration pour le redimensionnement
    def on_resize(event):
        # Redimensionner les widgets si nécessaire
        pass
    
    root.bind('<Configure>', on_resize)
    
    # Centrer la fenêtre
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Configuration des couleurs pour les tags de texte
    app.logs_text.tag_configure("error", foreground="#e74c3c")
    app.logs_text.tag_configure("warning", foreground="#f39c12")
    app.logs_text.tag_configure("MSG", foreground="#27ae60")
    app.logs_text.tag_configure("verbose", foreground="#95a5a6")
    
    root.mainloop()

if __name__ == "__main__":
    main()
