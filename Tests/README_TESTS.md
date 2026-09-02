# DOCUMENTATION DES TESTS

## Vue d'ensemble

Ce dossier contient les tests du **Vérificateur de PDFs** et les fichiers PDF d’exemple.

La documentation technique (logs, analyse, corrections) se trouve dans `docs/`.

## Fichiers de tests

### `tests_vrais_donnees.bat`
- **Tests qui RÉUSSISSENT tous**
- Utilise vos vrais formats de fichiers
- Teste avec vos vraies données
- 6 tests basés sur votre code réel

### `tests_vrais_echecs.bat`
- **Tests qui ÉCHOUENT tous**
- Simule vos vraies erreurs
- Basé sur vos logs d'erreur réels
- 6 tests d'échec typiques

## Documentation des données

### `donnees_test_reelles.txt`
- **Toutes les vraies données** extraites de votre projet
- Noms de fichiers de vos logs
- Contenus PDF réels
- Regex utilisées
- Problèmes détectés

### `exemples_fichiers_test.txt`
- **Exemples détaillés** de chaque test
- Format des fichiers testés
- Résultats attendus vs obtenus
- Cas de normalisation

### `logs_erreurs_reels.txt`
- **Vrais messages d'erreur** de votre système
- Messages de succès
- Patterns d'erreur analysés
- Données utilisées pour créer les tests

## Comment utiliser

1. **Lancer les tests qui réussissent** :
   ```
   Double-clic sur tests_vrais_donnees.bat
   ```

2. **Lancer les tests qui échouent** :
   ```
   Double-clic sur tests_vrais_echecs.bat
   ```

3. **Consulter la documentation** :
   - Lire les fichiers .txt pour comprendre les données
   - Voir d'où viennent tous les exemples de test

## Données sources

Toutes les données de test proviennent de :
- ✅ Vos **vrais logs d'erreur**
- ✅ Vos **vrais noms de fichiers**
- ✅ Votre **vrai code** (regex, normalisation)
- ✅ Votre **vrai programme** (Elio_Muxis_V1)
- ✅ Vos **vrais chemins** système

**Aucune donnée fictive** - tout est extrait de votre projet réel !

## Format des résultats

Chaque test affiche :
```
Test X - Description
   Ce qui est TROUVÉ    : 'résultat_réel'
   Ce qui est ATTENDU   : 'résultat_attendu'
   RÉSULTAT : RÉUSSI/ÉCHOUÉ
```

## Tests créés

### Tests de réussite (6)
1. Fichier 25.004_SN1000_1310.pdf
2. Fichier 25.004_SN1004_1310.pdf  
3. Fichier 23.270D SN 240 1310.pdf
4. Programme Elio_Muxis_V1.rule
5. Normalisation SN41_SE
6. Normalisation Elio_Muxis_V1

### Tests d'échec (6)
1. Fichier sans SN
2. Contenu PDF sans programme
3. SN différent nom vs contenu
4. Mauvais programme attendu
5. Fichier avec FAIL
6. Format SN impossible

Tous basés sur vos vraies données !
