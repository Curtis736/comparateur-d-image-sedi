# GUIDE DES LOGS EXPLICATIFS

## Vue d'ensemble

Le système de logs a été amélioré pour expliquer **exactement** ce qui est analysé et pourquoi certaines décisions sont prises.

## Niveaux de logs

- **[MSG]** : Messages d'information importants (résultats finaux)
- **[WARN]** : Avertissements (plusieurs SN/programmes trouvés, etc.)
- **[ERROR]** : Erreurs détectées
- **[VERB]** : Détails de l'analyse (nouveau !)

## Exemple de logs avec détails

### Analyse du SN

```
[MSG] Traitement du fichier: SN37-24-01.pdf
[VERB] SN détecté dans le nom du fichier: '37-24-01'
[VERB] SN normalisé pour comparaison: '37-24-01'
[VERB] Extraction du texte du PDF: SN37-24-01.pdf
[VERB] Texte extrait: 1234 caractères
[VERB] Analyse SN pour SN37-24-01.pdf: SN du nom = '37-24-01', normalisé = '37-24-01'
[VERB] Recherche du SN dans le texte avec variations: ['37-24-01', '37.24.01', '37-24-01']...
[VERB] Variation '37.24.01' trouvée dans le texte
[VERB] SN détectés par regex dans le PDF: ['37.24.01', '4103434784-557-10']
[VERB] Comparaison: SN candidat '37.24.01' normalisé = '37-24-01' vs attendu '37-24-01'
[VERB] SN correspondant trouvé: '37.24.01' (normalisé: '37-24-01')
[VERB] Comparaison finale SN: nom '37-24-01' normalisé = '37-24-01' vs PDF '37.24.01' normalisé = '37-24-01'
[MSG] SN: ok
```

### Analyse du programme

```
[VERB] Analyse programme pour SN37-24-01.pdf: Programme attendu = 'Elio_Muxis_V1', normalisé = 'elio_muxis_v1'
[VERB] Recherche directe du programme dans le texte avec variations: ['elio_muxis_v1', 'elio muxis v1', 'elio_muxis_v1.rule']...
[VERB] Programme trouvé directement dans le texte: 'elio muxis v1.rule'
[MSG] Programme: ok
```

### Cas avec plusieurs SN

```
[VERB] Recherche parmi tous les SN trouvés: ['37.24.01', '4103434784-557-10']
[VERB] Comparaison: '37.24.01' normalisé = '37-24-01' vs attendu '37-24-01'
[MSG] SN correspondant trouvé: '37.24.01' (normalisé: '37-24-01')
```

### Cas avec plusieurs programmes

```
[VERB] Programmes détectés par regex dans le PDF: ['V1.rule', 'Elio Muxis V1.rule']
[VERB] Recherche du programme correspondant exactement...
[VERB] Comparaison: programme 'V1.rule' normalisé = 'v1' vs attendu 'elio_muxis_v1'
[VERB] Comparaison: programme 'Elio Muxis V1.rule' normalisé = 'elio muxis v1' vs attendu 'elio_muxis_v1'
[VERB] Aucun programme ne correspond exactement, filtrage des programmes partiels...
[VERB] Programmes après filtrage (longueur >= 8): ['Elio Muxis V1.rule']
[VERB] Programme le plus long sélectionné: 'Elio Muxis V1.rule'
[VERB] Le programme complet 'Elio Muxis V1.rule' contient le nom attendu 'elio_muxis_v1'
[WARN] Plusieurs programmes trouvés dans SN37-24-01.pdf: ['V1.rule', 'Elio Muxis V1.rule']. Programme partiel ignoré, utilisation du programme complet: Elio Muxis V1.rule
[MSG] Programme: ok
```

## Ce que vous pouvez comprendre maintenant

### Pour le SN :
1. **Quel SN est détecté** dans le nom de fichier
2. **Comment il est normalisé** (enlève .pdf, convertit points en tirets)
3. **Quels SN sont trouvés** dans le PDF
4. **Quelles comparaisons** sont faites
5. **Pourquoi un SN est choisi** plutôt qu'un autre

### Pour le programme :
1. **Quel programme est attendu** et sa forme normalisée
2. **Quelles variations** sont recherchées dans le texte
3. **Quels programmes sont détectés** par le regex
4. **Pourquoi un programme est choisi** (correspond exactement, plus long, contient le nom, etc.)
5. **Quels programmes partiels sont ignorés** et pourquoi

## Comment utiliser ces logs

### Pour déboguer :
- Activez les logs VERB dans votre interface
- Suivez le processus étape par étape
- Comprenez pourquoi une décision est prise

### Pour comprendre les erreurs :
- Regardez les comparaisons faites
- Voyez quels SN/programmes sont trouvés
- Comprenez pourquoi ils ne correspondent pas

### Pour valider :
- Vérifiez que les bonnes variations sont recherchées
- Confirmez que les normalisations sont correctes
- Validez que les bons éléments sont sélectionnés

## Exemple complet d'analyse

```
[MSG] Traitement du fichier: SN37-24-01.pdf
[VERB] SN détecté dans le nom du fichier: '37-24-01'
[VERB] SN normalisé pour comparaison: '37-24-01'
[VERB] Extraction du texte du PDF: SN37-24-01.pdf
[VERB] Texte extrait: 2500 caractères
[VERB] Analyse SN pour SN37-24-01.pdf: SN du nom = '37-24-01', normalisé = '37-24-01'
[VERB] Recherche du SN dans le texte avec variations: ['37-24-01', '37.24.01', '37-24-01']...
[VERB] Variation '37.24.01' trouvée dans le texte
[VERB] SN détectés par regex dans le PDF: ['37.24.01', '4103434784-557-10']
[VERB] Comparaison: SN candidat '37.24.01' normalisé = '37-24-01' vs attendu '37-24-01'
[VERB] SN correspondant trouvé: '37.24.01' (normalisé: '37-24-01')
[VERB] Comparaison finale SN: nom '37-24-01' normalisé = '37-24-01' vs PDF '37.24.01' normalisé = '37-24-01'
[MSG] SN: ok
[VERB] Analyse programme pour SN37-24-01.pdf: Programme attendu = 'Elio_Muxis_V1', normalisé = 'elio_muxis_v1'
[VERB] Recherche directe du programme dans le texte avec variations: ['elio_muxis_v1', 'elio muxis v1', 'elio_muxis_v1.rule']...
[VERB] Programme trouvé directement dans le texte: 'elio muxis v1.rule'
[MSG] Programme: ok
[MSG] Conformité: ok
```

**Maintenant vous savez EXACTEMENT ce qui est analysé et pourquoi !**