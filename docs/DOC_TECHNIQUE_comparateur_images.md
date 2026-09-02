# comparateur_image - Documentation Technique des pages

## Vue d'ensemble

Cette documentation decrit, page par page, l'architecture fonctionnelle et technique de l'application de verification PDF.

**Perimetre code**
- `src/inferface.py` (interface Tkinter)
- `src/VerifPdfRoutine.py` (orchestration metier)
- `src/VerifPdf.py` (extraction texte + regex)
- `src/Log.py` (journalisation + callbacks)

---

## Sommaire

1. [Fenetre principale](#1-fenetre-principale---verificateur-de-pdfs)
2. [Page Logs en temps reel](#2-page-logs-en-temps-reel)
3. [Page Resume](#3-page-resume)
4. [Page Fichiers](#4-page-fichiers)
5. [Fenetres de dialogue](#5-fenetres-de-dialogue-modales)
6. [Page Rapport exporte](#6-page-rapport-exporte-fichier-texte)
7. [Services backend utilises par les pages](#7-services-backend-utilises-par-les-pages)
8. [Carte des evenements UI -> backend](#8-carte-des-evenements-ui---backend)
9. [Ameliorations recommandees](#9-ameliorations-recommandees)

---

## 1) Fenetre principale - "Verificateur de PDFs"

### Finalite
Conteneur principal de l'application. Cette fenetre rassemble la configuration, les commandes utilisateur, les onglets de sortie et l'etat global du traitement.

### Point d'entree
| Element | Valeur |
|---|---|
| Classe UI | `InterfaceVerificationPDF` |
| Initialisation | `__init__(self, root)` |
| Lancement app | `main()` dans `src/inferface.py` |

### Composition visuelle
| Zone | Description |
|---|---|
| Titre | Label principal "Verificateur de PDFs" |
| Configuration | Dossier (readonly + bouton parcourir), Programme attendu (`Elio_Muxis_V1`, readonly) |
| Actions | Demarrer / Arreter / Effacer les logs / Sauvegarder rapport |
| Resultats | Notebook: Logs, Resume, Fichiers |
| Statut | Barre de progression + texte d'etat + compteurs |

### Dependances
- `tkinter`, `ttk`, `scrolledtext`, `filedialog`, `messagebox`
- `threading` (eviter le blocage de l'interface)
- `Log` (bus d'evenements de log)

### Cycle nominal
1. Selection d'un dossier.
2. Detection et affichage des PDF dans l'onglet Fichiers.
3. Lancement de la verification dans un thread dedie.
4. Remontee des logs backend vers l'UI.
5. Generation du resume en fin de run.

### Limites connues
- Le bouton **Arreter** ne coupe pas activement la routine metier.
- Les compteurs affiches sont informatifs, pas metiers.
- Nom de fichier historique: `src/inferface.py`.

---

## 2) Page "Logs en temps reel"

### Finalite
Afficher les messages de verification en streaming avec une visualisation par niveau de severite.

### Composant principal
- `ScrolledText`: `self.logs_text`

### Source de donnees
Callbacks enregistres sur `Log.py`:
- `MSG` -> `add_log_message`
- `WARN` -> `add_log_warning`
- `ERR` -> `add_log_error`
- `VERB` -> `add_log_verbose`

### Regles d'affichage
| Niveau | Prefixe log | Tag UI | Couleur |
|---|---|---|---|
| Information | `[MSG]` | `MSG` | Vert |
| Avertissement | `[WARN]` | `warning` | Orange |
| Erreur | `[ERROR]` | `error` | Rouge |
| Verbose | `[VERB]` | `verbose` | Gris |

### Contrainte technique importante
Les mises a jour UI sont faites via `self.root.after(0, ...)` pour conserver la securite thread Tkinter.

### Maintenance
Si un nouveau niveau de log apparait, il faut mettre a jour:
1. `setup_log_callbacks()`
2. `_add_log(...)`
3. la configuration des tags visuels

---

## 3) Page "Resume"

### Finalite
Fournir un bilan lisible de la session de verification.

### Composant principal
- `ScrolledText`: `self.summary_text`

### Strategie de calcul
Le resume est reconstruit via `create_summary()` en parsant le texte de `self.logs_text`:
- comptage occurrences `"[ERROR]"`
- comptage occurrences `"[WARN]"`
- comptage occurrences `"[MSG]"`

### Sections produites
- Contexte (dossier, programme attendu)
- Statistiques
- Liste des erreurs detectees
- Liste des avertissements
- Recommandations automatiques

### Limite
Le mecanisme depend du format texte des logs (pas de modele de donnees structure).

---

## 4) Page "Fichiers"

### Finalite
Lister les PDF du dossier et ouvrir rapidement le document selectionne.

### Composants
- `Listbox`: `self.files_listbox`
- Bouton "Ouvrir le PDF"

### Alimentation
Lors de `select_folder()`:
1. scan du dossier (`os.listdir`)
2. filtrage extension `.pdf`
3. alimentation de `self.pdf_paths` (chemins absolus)
4. affichage des noms dans la listbox

### Interactions
| Action utilisateur | Handler |
|---|---|
| Double-clic sur un fichier | `on_open_selected_pdf()` |
| Clic "Ouvrir le PDF" | `open_selected_pdf()` |
| Execution systeme | `open_pdf(path)` |

### Ouverture cross-plateforme
- Windows: `os.startfile(path)`
- macOS: `subprocess.run(["open", path])`
- Linux: `subprocess.run(["xdg-open", path])`

### Limites
- Risque de desynchronisation listbox / `self.pdf_paths` si etat externe change.
- Aucun refresh automatique si le dossier est modifie apres chargement.

---

## 5) Fenetres de dialogue (modales)

### Finalite
Gerer les interactions systeme et les validations bloquantes.

### Inventaire
| API | Usage |
|---|---|
| `filedialog.askdirectory` | Choix du dossier source |
| `filedialog.asksaveasfilename` | Choix du chemin de rapport |
| `messagebox.showwarning` | Preconditions non satisfaites |
| `messagebox.showinfo` | Confirmation d'action |
| `messagebox.showerror` | Erreur bloquante |

### Scenarios couverts
- dossier absent
- verification deja en cours
- sauvegarde reussie / echouee
- echec d'ouverture d'un PDF

---

## 6) Page "Rapport exporte" (fichier texte)

### Finalite
Exporter un artefact textuel de verification partageable.

### Generation
- Methode: `save_report()`
- Encodage: UTF-8
- Extension: `.txt`

### Structure du rapport
1. Entete
2. Metadonnees (dossier, programme, date)
3. Logs complets
4. Resume

### Limite
Format non structure (pas de JSON/CSV), peu adapte au traitement automatise.

---

## 7) Services backend utilises par les pages

### 7.1 Verification metier
**Fonction:** `VerifPdfRoutine.VerifyFolder(path, program)`

Controles executes par fichier PDF:
1. SN present dans le nom
2. Texte extractible depuis le PDF
3. SN trouve dans le contenu (avec normalisation)
4. Programme `.rule` coherent avec l'attendu
5. Absence du mot-cle `FAIL`

### 7.2 Normalisation SN
**Fonction:** `_normalize_sn(sn)` dans `src/VerifPdfRoutine.py`

Regles:
- suppression suffixes `_SE`, `_E`, `_RCI`
- conversion `.` vers `-`
- reduction du format `NNNN_VVV` (ex: `1073_940`) vers SN base `1073`

### 7.3 Extraction texte + detection
**Module:** `src/VerifPdf.py`
- `GetPdfText(path)` via `pypdf`
- `SN_REGEX` pour detection serial
- `PROG_REGEX` pour detection programmes `.rule`

### 7.4 Journalisation
**Module:** `Log.py`
- buffer memoire `logBuffer`
- callbacks par niveau vers l'UI
- possibilite d'export via `CreateLogFile(...)`

---

## 8) Carte des evenements UI -> backend

| Action UI | Methode UI | Backend impacte |
|---|---|---|
| Parcourir | `select_folder()` | Scan PDF + logs + alimentation page Fichiers |
| Demarrer | `start_verification()` -> `run_verification()` | `VerifPdfRoutine.VerifyFolder(...)` |
| Arreter | `stop_verification()` | Etat UI + message log |
| Effacer les logs | `clear_logs()` | Reset Logs + Resume |
| Sauvegarder rapport | `save_report()` | Export texte |
| Ouvrir PDF | `open_pdf(path)` | Lecteur systeme |

---

## 9) Ameliorations recommandees

### Priorite haute
- Renommer `src/inferface.py` en `src/interface.py` pour clarte et maintenance.
- Introduire un objet resultat structure pour remplacer le parsing de texte du resume.
- Ajouter une annulation cooperative dans `VerifyFolder(...)` pour rendre **Arreter** reellement effectif.

### Priorite moyenne
- Ajouter des tests unitaires sur:
  - `_normalize_sn`
  - `GetSnFromString`
  - `GetAllProgsFromString`
- Ajouter un export machine (`JSON`) pour usage QA/SI.


