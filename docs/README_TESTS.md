# README - Tests Unitaires

## Vue d'ensemble

Ce projet contient **deux types de tests unitaires** pour vérifier le bon fonctionnement du Vérificateur de PDFs :

1. **`test_comparateur_image.py`** - Tests unitaires complets et professionnels
2. **`tests_faciles.py`** - Tests simplifiés avec interface utilisateur conviviale

## Fichier 1 : `test_comparateur_image.py`

### Description
Tests unitaires **complets et professionnels** utilisant le framework `unittest` de Python.

### Caractéristiques
- **Framework standard** : Utilise `unittest` (inclus avec Python)
- **Tests exhaustifs** : Couvre tous les modules et fonctions
- **Mocking avancé** : Simule les fichiers PDF et les erreurs
- **Tests d'intégration** : Vérifie le fonctionnement global
- **Rapports détaillés** : Sortie professionnelle avec statistiques

### Modules testés
- `Log.py` - Système de journalisation
- `VerifPdf.py` - Extraction et analyse des PDFs
- `VerifPdfRoutine.py` - Logique de vérification des dossiers
- Tests d'intégration complets

### Comment l'utiliser
```bash
python test_comparateur_image.py
```

### Exemple de sortie
```
test_get_sn_from_string_valid (__main__.TestVerifPdf) ... ok
test_log_levels (__main__.TestLog) ... ok
test_normalize_program_name (__main__.TestVerifPdfRoutine) ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.123s

OK
```

### Avantages
- ✅ Tests très détaillés et robustes
- ✅ Détection précise des régressions
- ✅ Couverture complète du code
- ✅ Format standard reconnu par les IDEs

### Inconvénients
- ❌ Plus complexe à comprendre pour les débutants
- ❌ Sortie technique moins lisible
- ❌ Nécessite des connaissances en tests unitaires

---

## Fichier 2 : `tests_faciles.py`

### Description
Tests unitaires **simplifiés et conviviaux** avec interface utilisateur claire.

### Caractéristiques
- **Interface simple** : Messages clairs et compréhensibles
- **Pas de framework** : Code Python pur, facile à modifier
- **Explications détaillées** : Chaque test explique ce qu'il fait
- **Tests volontaires d'échec** : Montre la différence entre succès et échec
- **Résumé visuel** : Statistiques claires en fin d'exécution

### Modules testés
- Détection des SN dans les noms de fichiers
- Détection des programmes .rule
- Normalisation des SN et programmes
- Système de logs
- Gestion des dossiers vides et fichiers non-PDF

### Comment l'utiliser
```bash
python tests_faciles.py
```
Ou double-clic sur `lancer_tests.bat`

### Exemple de sortie
```
Test : Détection SN dans noms de fichiers
   Test des cas valides...
      OK 'SN12345_document.pdf' -> '12345'
      OK 'fichier_SN67890.pdf' -> '67890'
   RÉUSSI

RÉSUMÉ DES TESTS
==================================================
Tests réussis : 7/9
Tests échoués : 2/9

PARFAIT ! Tous les tests sont passés !
(Les échecs sont volontaires pour la démonstration)
```

### Avantages
- ✅ Très facile à comprendre
- ✅ Messages clairs et explicites
- ✅ Montre les cas d'échec volontaires
- ✅ Parfait pour les débutants
- ✅ Facile à modifier et étendre

### Inconvénients
- ❌ Moins exhaustif que les tests professionnels
- ❌ Pas de mocking avancé
- ❌ Format non-standard

---

## Comparaison des deux approches

| Critère | `test_comparateur_image.py` | `tests_faciles.py` |
|---------|----------------------------|-------------------|
| **Niveau** | Professionnel | Débutant |
| **Framework** | unittest | Code personnalisé |
| **Lisibilité** | Technique | Très claire |
| **Exhaustivité** | Complète | Basique |
| **Facilité d'usage** | Moyenne | Très facile |
| **Maintenance** | Standard | Simple |
| **Apprentissage** | Difficile | Facile |

## Quand utiliser chaque test ?

### Utilisez `test_comparateur_image.py` si :
- Vous développez professionnellement
- Vous voulez une couverture complète
- Vous intégrez dans un pipeline CI/CD
- Vous connaissez les tests unitaires

### Utilisez `tests_faciles.py` si :
- Vous débutez avec les tests
- Vous voulez comprendre rapidement les problèmes
- Vous préférez une interface simple
- Vous voulez voir des exemples d'échecs

## Fichiers de support

### `lancer_tests.bat`
Script Windows pour lancer `tests_faciles.py` facilement :
- Double-clic pour exécuter
- Vérifications automatiques (Python installé, fichiers présents)
- Messages d'erreur clairs
- Pause automatique pour voir les résultats

### `GUIDE_TESTS.md`
Guide complet pour comprendre et utiliser les tests :
- Instructions détaillées
- Exemples concrets
- Dépannage
- Conseils pour débutants

## Installation et prérequis

### Prérequis communs
- Python 3.7 ou supérieur
- Modules du projet : `Log.py`, `VerifPdf.py`, `VerifPdfRoutine.py`

### Prérequis pour `test_comparateur_image.py`
```bash
# Aucune installation supplémentaire nécessaire
# unittest est inclus avec Python
```

### Prérequis pour `tests_faciles.py`
```bash
# Aucune installation supplémentaire nécessaire
# Code Python pur
```

## Recommandations

### Pour les développeurs débutants
1. **Commencez par** `tests_faciles.py`
2. **Comprenez** les messages d'erreur
3. **Expérimentez** avec les tests volontaires d'échec
4. **Passez ensuite** à `test_comparateur_image.py`

### Pour les développeurs expérimentés
1. **Utilisez** `test_comparateur_image.py` pour le développement
2. **Gardez** `tests_faciles.py` pour les démonstrations
3. **Intégrez** les tests dans votre workflow
4. **Étendez** les tests selon vos besoins

### Pour les équipes mixtes
1. **Formation** avec `tests_faciles.py`
2. **Production** avec `test_comparateur_image.py`
3. **Documentation** avec les deux approches
4. **Maintenance** simplifiée grâce aux deux niveaux

## Conclusion

Les deux fichiers de tests sont **complémentaires** :
- `test_comparateur_image.py` pour la **robustesse technique**
- `tests_faciles.py` pour la **compréhension et l'apprentissage**

Utilisez celui qui correspond le mieux à votre niveau et à vos besoins !




