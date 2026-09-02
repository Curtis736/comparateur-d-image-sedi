# Vérificateur de PDFs — Contrôle SN et Programmes (.rule)

## Objectif
Cette application vérifie automatiquement des fichiers PDF dans un dossier en contrôlant :
- **SN dans le nom de fichier**: présence d’un numéro de série (préfixé par `SN`)
- **SN dans le contenu**: présence du même SN à l’intérieur du PDF
- **Programme attendu**: présence d’un nom de programme se terminant par `.rule` dans le PDF, identique à celui saisi dans l’interface
- **Conformité**: absence du mot-clé `FAIL` dans le contenu du PDF

## Installation
- **Prérequis**: Python 3.7+
- **Dépendances**:
```bash
pip install -r requirements.txt
```
Si l’installation échoue à cause de `tkinter`, supprimez la ligne `tkinter` de `requirements.txt` (Tkinter est livré avec Python sur Windows et ne s’installe pas via pip).

## Lancement rapide
Double-clic sur `comparateur_image.bat`, ou :
```bash
python src/inferface.py
```

## Utilisation
1. Cliquez sur **📂 Parcourir** et sélectionnez le dossier contenant vos PDFs.
2. Le **Programme attendu** est fixé en lecture seule à `Elio_Muxis_V1`.
3. Cliquez sur **🔍 Démarrer la vérification**.
4. Suivez l’avancement dans l’onglet **📝 Logs en temps réel** et consultez le **📋 Résumé** à la fin.
5. Optionnel: **💾 Sauvegarder rapport** pour exporter les logs et le résumé dans un fichier texte.

## Vérifications et logs "ok"
- **SN: ok**
  - Un SN est présent dans le nom du fichier et retrouvé identique dans le contenu du PDF (ou en recherche flexible insensible à la casse). Les désignations terminales `_SE` et `_E` dans le nom de fichier ou dans le PDF sont ignorées pour la comparaison (ex: `SN41_SE` ≡ `SN41`).
- **Programme: ok**
  - Le PDF contient le programme attendu `Elio_Muxis_V1`, accepté avec ou sans le suffixe `.rule` (ex: `Elio_Muxis_V1` ou `Elio_Muxis_V1.rule`). La comparaison est insensible à la casse.
- **Conformité: ok**
  - Le mot `FAIL` n’apparaît pas dans le PDF.

Lignes d’information affichées pendant l’exécution:
- `Traitement du fichier: <nom.pdf>`
- `Programme attendu: Elio_Muxis_V1`
- `Nombre de fichiers PDF à vérifier: <n>`

## Comment ça marche (interne)
Voici, étape par étape, ce que fait l’application pour chaque fichier du dossier :
1. **Filtrage**: ne traite que les fichiers se terminant par `.pdf`. Tout autre fichier est signalé en erreur.
2. **SN dans le nom**: recherche `SN` suivi d’un identifiant (lettres/chiffres/tiret) dans le nom de fichier via le motif:
   - `SN\s*([\w-]+)`
3. **Extraction du texte**: lit le PDF avec `pypdf` et concatène le texte extrait de chaque page.
4. **SN dans le contenu**: applique le même motif au texte du PDF et compare au SN du nom de fichier. Une recherche flexible insensible à la casse peut valider le SN. La comparaison ignore les suffixes `_SE` et `_E`.
5. **Programme (Elio_Muxis_V1)**: recherche un programme via le motif:
   - `[\w,-]+\.rule`
   Puis valide contre le programme attendu fixé `Elio_Muxis_V1`. La comparaison est normalisée (sans suffixe `.rule`) et insensible à la casse. Si aucun `.rule` n’est trouvé, une présence simple de `Elio_Muxis_V1` dans le texte est acceptée.
6. **Mot-clé FAIL**: si `FAIL` est trouvé dans le texte, le fichier est marqué en non conforme.
7. **Journalisation**: messages courts `SN: ok`, `Programme: ok`, `Conformité: ok` lorsque les contrôles passent; erreurs/avertissements explicites sinon.

## Ce qu’il faut mettre dans "Programme attendu"
- Le programme attendu est désormais **fixé** à `Elio_Muxis_V1` (champ en lecture seule dans l’interface).
- Formes acceptées dans le PDF: `Elio_Muxis_V1` ou `Elio_Muxis_V1.rule` (insensible à la casse).

## Interface
- **Configuration**: sélection du dossier; programme attendu fixé en lecture seule à `Elio_Muxis_V1`
- **Contrôles**: démarrer/arrêter, effacer les logs, sauvegarder rapport
- **Résultats**:
  - Onglet **📝 Logs en temps réel** (flux détaillé)
  - Onglet **📋 Résumé** (statistiques, erreurs, avertissements, recommandations)
- **Compteurs**: affichage approximatif du nombre de fichiers traités et du nombre de messages/erreurs

## Structure du projet
- `comparateur_image.bat` : Lancement Windows
- `src/` : Code source
  - `inferface.py` : Interface graphique principale (Tkinter)
  - `VerifPdf.py` : Extraction du texte PDF et détection (SN, programme)
  - `VerifPdfRoutine.py` : Routine de vérification d’un dossier
  - `Log.py` : Système de logs avec callbacks
- `docs/` : Documentation technique
- `Tests/` : Scripts de test et PDF d’exemple (`Tests/Fichiers_Test/`)
- `requirements.txt` : Dépendances Python

## Format attendu des fichiers
- Extension `.pdf`
- Le nom du fichier doit contenir un **SN** (ex: `SN12345_document.pdf`)
- Le PDF doit contenir le **même SN** dans son texte (les suffixes `_SE` et `_E` peuvent être ignorés)
- Le PDF doit contenir le programme `Elio_Muxis_V1` (avec ou sans suffixe `.rule`)

### Exemple de nom de fichier
```
SN41_SE_Elio_Muxis_V1.rule.pdf
```

## Messages d’erreur typiques
- `Pas de SN détecté dans le nom du fichier ...`
- `Impossible d'extraire le texte du fichier ...`
- `N'a pas pu trouver le SN dans le pdf ...`
- `Le fichier ... a SN[X] dans le nom mais SN[Y] à l'intérieur`
- `N'a pas pu trouver le programme dans le pdf ...`
- `Le fichier ... n'a pas le bon programme ...`
- `Le fichier ... n'est pas dans les specs` (présence de `FAIL`)

## Dépannage
- **Échec d’installation de tkinter**: supprimez `tkinter` de `requirements.txt`. Tkinter est inclus avec Python.
- **Aucun texte extrait**: certains PDFs (scans) n’ont pas de texte. Il faut un OCR en amont (non inclus ici).
- **Comparaison du programme**: la comparaison est désormais insensible à la casse et accepte la forme sans `.rule` pour `Elio_Muxis_V1`.
- **Encodage**: utilisez des noms de fichier et contenus en UTF-8 lorsque possible.

## Évolutions possibles
- Détecter automatiquement le programme attendu depuis le premier PDF du dossier
- Améliorer la robustesse de l’extraction texte page par page

## Licence
Usage interne/privé (à adapter selon vos besoins). 