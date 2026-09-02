FICHIERS PDF DE TEST
===================

Ce dossier contient les vrais fichiers PDF utilisés pour tester votre vérificateur.

FICHIERS QUI MARCHENT (pour tests de réussite)
==============================================

25.004_SN1000_1310.pdf
├── SN dans nom : 1000_1310
├── SN dans contenu : SN1000_1310
├── Programme : Elio_Muxis_V1.rule
├── FAIL : Non
└── Résultat attendu : SUCCÈS

25.004_SN1004_1310.pdf
├── SN dans nom : 1004_1310
├── SN dans contenu : SN1004_1310
├── Programme : Elio_Muxis_V1.rule
├── FAIL : Non
└── Résultat attendu : SUCCÈS

23.270D SN 240 1310.pdf
├── SN dans nom : 240
├── SN dans contenu : SN 240
├── Programme : Elio_Muxis_V1.rule
├── FAIL : Non
└── Résultat attendu : SUCCÈS

FICHIERS QUI NE MARCHENT PAS (pour tests d'échec)
=================================================

document_sans_sn.pdf
├── SN dans nom : Aucun
├── SN dans contenu : Aucun
├── Programme : Aucun
├── FAIL : Non
└── Résultat attendu : ÉCHEC (pas de SN)

fichier_avec_fail.pdf
├── SN dans nom : Aucun dans le nom
├── SN dans contenu : SN123
├── Programme : Elio_Muxis_V1.rule
├── FAIL : Oui (contient "FAIL")
└── Résultat attendu : ÉCHEC (non conforme)

fichier_avec_V1_rule.pdf
├── SN dans nom : Aucun dans le nom (à tester avec nom approprié)
├── SN dans contenu : SN37-24-01
├── Programme : Contient "V1.rule" ET "Elio_Muxis_V1.rule"
├── FAIL : Non
├── Problème : Teste la logique de sélection du bon programme
├── Résultat attendu : SUCCÈS (doit trouver Elio_Muxis_V1.rule, pas V1.rule)
└── But : Tester la correction du problème de programme partiel

COMMENT TESTER AVEC CES FICHIERS
================================

1. Lancez l'application (comparateur_image.bat à la racine du projet)
2. Sélectionnez le dossier : Tests/Fichiers_Test/
3. Lancez la vérification
4. Comparez les résultats avec les attentes ci-dessus

OU

1. Utilisez les tests automatiques (.bat)
2. Ils testent les noms et contenus sans avoir besoin des vrais fichiers
3. Mais maintenant vous avez les vrais fichiers pour tester manuellement

CONTENU DES PDF
===============

Tous les PDF contiennent du texte lisible :
- Titre : "Rapport de test"
- SN : Le numéro de série correspondant
- Programme : "Elio_Muxis_V1.rule" (sauf document_sans_sn.pdf)
- Statut : "PASS" ou "FAIL"

Ces fichiers sont de VRAIS PDF que votre code peut lire avec pypdf !
