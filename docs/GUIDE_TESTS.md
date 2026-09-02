# 🧪 GUIDE COMPLET DES TESTS UNITAIRES

## 📋 Qu'est-ce que c'est ?

Les **tests unitaires** sont comme des "vérifications automatiques" de votre code. Imaginez que vous avez une calculatrice : les tests vont vérifier que 2+2 = 4, que 5-3 = 2, etc.

Pour votre vérificateur de PDFs, les tests vont vérifier que :
- ✅ Il trouve bien les numéros SN dans les noms de fichiers
- ✅ Il détecte bien les programmes .rule
- ✅ Il gère bien les erreurs
- ✅ Tout fonctionne comme prévu

## 🚀 COMMENT LANCER LES TESTS (SUPER FACILE)

### Méthode 1 : Double-clic (Windows)
1. Ouvrez l'explorateur de fichiers
2. Allez dans le dossier de votre projet
3. **Double-cliquez** sur `tests_faciles.py`
4. Une fenêtre noire s'ouvre avec les résultats !

### Méthode 2 : Ligne de commande
1. **Ouvrez l'invite de commandes** :
   - Windows : Appuyez sur `Windows + R`, tapez `cmd`, appuyez sur Entrée
   - Ou clic droit dans le dossier → "Ouvrir dans le terminal"

2. **Naviguez vers votre dossier** :
   ```bash
   cd "X:\Production\4_Public\DEV (ne pas toucher)\comparateur_image"
   ```

3. **Lancez les tests** :
   ```bash
   python tests_faciles.py
   ```

## 📊 COMPRENDRE LES RÉSULTATS

### ✅ Quand tout va bien :
```
🔍 Test : Détection SN dans noms de fichiers
   📝 Test des cas valides...
      ✅ 'SN12345_document.pdf' → '12345'
      ✅ 'fichier_SN67890.pdf' → '67890'
   ✅ RÉUSSI

📊 RÉSUMÉ DES TESTS
==================================================
✅ Tests réussis : 7/7
❌ Tests échoués : 0/7

🎉 PARFAIT ! Tous les tests sont passés !
```

### ❌ Quand il y a un problème :
```
🔍 Test : Détection SN dans noms de fichiers
   📝 Test des cas valides...
      ❌ 'SN12345_document.pdf' → attendu '12345', trouvé 'None'
   ❌ ÉCHOUÉ

📊 RÉSUMÉ DES TESTS
==================================================
✅ Tests réussis : 6/7
❌ Tests échoués : 1/7

⚠️  Il y a 1 problème(s) à corriger :
   • Détection SN dans noms de fichiers: ...
```

## 🔧 QUE FAIRE SI UN TEST ÉCHOUE ?

### 1. **Lisez le message d'erreur**
Le test vous dit exactement ce qui ne va pas :
- `attendu '12345', trouvé 'None'` = la fonction devrait trouver "12345" mais ne trouve rien

### 2. **Vérifiez le code correspondant**
- Problème de SN → regardez dans `VerifPdf.py` la fonction `GetSnFromString`
- Problème de programme → regardez `GetProgFromString`
- Problème de logs → regardez dans `Log.py`

### 3. **Testez manuellement**
Ouvrez Python et testez :
```python
import VerifPdf
result = VerifPdf.GetSnFromString("SN12345_test.pdf")
print(result)  # Devrait afficher "12345"
```

## 📝 TESTS DISPONIBLES

| Test | Ce qu'il vérifie | Fichier testé |
|------|------------------|---------------|
| **Détection SN** | Trouve les SN dans les noms | `VerifPdf.py` |
| **Détection programmes** | Trouve les .rule | `VerifPdf.py` |
| **Normalisation SN** | Enlève _SE et _E | `VerifPdfRoutine.py` |
| **Normalisation programmes** | Minuscules, enlève .rule | `VerifPdfRoutine.py` |
| **Système logs** | Messages bien enregistrés | `Log.py` |
| **Dossier vide** | Gère les dossiers sans PDF | `VerifPdfRoutine.py` |
| **Fichiers non-PDF** | Ignore les .txt, .doc, etc. | `VerifPdfRoutine.py` |

## 🎯 EXEMPLES CONCRETS

### Test de détection SN
```python
# Ces cas DOIVENT marcher :
"SN12345_document.pdf" → trouve "12345" ✅
"rapport_SN999.pdf" → trouve "999" ✅

# Ces cas NE DOIVENT PAS marcher :
"pas_de_sn.pdf" → trouve rien ✅
"SN.pdf" → trouve rien ✅
```

### Test de normalisation
```python
# Normalisation des SN :
"SN123_SE" → devient "SN123" ✅
"SN456_E" → devient "SN456" ✅
"SN789" → reste "SN789" ✅

# Normalisation des programmes :
"Elio_Muxis_V1.rule" → devient "elio_muxis_v1" ✅
"PROGRAMME.RULE" → devient "programme" ✅
```

## 🆘 DÉPANNAGE

### "python n'est pas reconnu"
**Problème** : Python n'est pas installé ou pas dans le PATH
**Solution** : 
1. Vérifiez que Python est installé : `python --version`
2. Ou utilisez : `py tests_faciles.py`

### "No module named 'VerifPdf'"
**Problème** : Les fichiers ne sont pas dans le bon dossier
**Solution** : Assurez-vous que tous ces fichiers sont ensemble :
- `tests_faciles.py`
- `VerifPdf.py`
- `VerifPdfRoutine.py`
- `Log.py`

### "Permission denied"
**Problème** : Droits insuffisants
**Solution** : Lancez l'invite de commandes en tant qu'administrateur

## 🎓 POUR ALLER PLUS LOIN

### Ajouter vos propres tests
Vous pouvez ajouter des tests dans `tests_faciles.py` :

```python
def mon_nouveau_test():
    """Test personnalisé"""
    # Votre logique de test ici
    return True  # ou False si échec

# Dans main(), ajouter :
testeur.tester("Mon nouveau test", mon_nouveau_test)
```

### Tests automatiques
Pour lancer les tests automatiquement à chaque modification, créez un fichier `.bat` :

```batch
@echo off
echo Lancement des tests...
python tests_faciles.py
pause
```

## 📞 AIDE

Si vous avez des questions :
1. **Lisez les messages d'erreur** - ils sont très explicites
2. **Testez une fonction à la fois** - isolez le problème
3. **Vérifiez que tous les fichiers sont présents**
4. **Relancez les tests après chaque correction**

---

**💡 Conseil** : Lancez les tests AVANT de modifier votre code pour vous assurer qu'ils passent, puis après chaque modification pour vérifier que vous n'avez rien cassé !




