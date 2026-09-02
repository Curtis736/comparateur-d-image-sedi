@echo off
cd /d "%~dp0"
echo TESTS QUI ÉCHOUENT AVEC VOS VRAIES DONNÉES
echo ==========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR - Python non trouvé
    pause
    exit /b 1
)

REM Créer le test directement dans le .bat
echo import sys > test_echec_temp.py
echo import os >> test_echec_temp.py
echo sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")) >> test_echec_temp.py
echo. >> test_echec_temp.py
echo try: >> test_echec_temp.py
echo     import VerifPdf >> test_echec_temp.py
echo     import VerifPdfRoutine >> test_echec_temp.py
echo except ImportError as e: >> test_echec_temp.py
echo     print(f"ERREUR - Import : {e}") >> test_echec_temp.py
echo     exit(1) >> test_echec_temp.py
echo. >> test_echec_temp.py
echo print("TESTS QUI ÉCHOUENT AVEC VOS VRAIES DONNÉES") >> test_echec_temp.py
echo print("=" * 45) >> test_echec_temp.py
echo. >> test_echec_temp.py
echo # Test 1 - Chercher SN dans fichier sans SN >> test_echec_temp.py
echo print("\nTest 1 - Fichier sans SN") >> test_echec_temp.py
echo print("   Fichier testé : document_rapport.pdf") >> test_echec_temp.py
echo sn1 = VerifPdf.GetSnFromString("document_rapport.pdf") >> test_echec_temp.py
echo print(f"   Ce qui est TROUVÉ    : '{sn1}'") >> test_echec_temp.py
echo print(f"   Ce qui est ATTENDU   : 'SN12345'") >> test_echec_temp.py
echo if sn1 == "SN12345": >> test_echec_temp.py
echo     print("   RÉSULTAT : RÉUSSI") >> test_echec_temp.py
echo else: >> test_echec_temp.py
echo     print("   RÉSULTAT : ÉCHOUÉ") >> test_echec_temp.py
echo. >> test_echec_temp.py
echo # Test 2 - Chercher programme inexistant >> test_echec_temp.py
echo print("\nTest 2 - Contenu PDF sans programme") >> test_echec_temp.py
echo print("   Contenu testé : Rapport de test sans programme") >> test_echec_temp.py
echo contenu_sans_prog = "Rapport de test sans programme" >> test_echec_temp.py
echo prog1 = VerifPdf.GetProgFromString(contenu_sans_prog) >> test_echec_temp.py
echo print(f"   Ce qui est TROUVÉ    : '{prog1}'") >> test_echec_temp.py
echo print(f"   Ce qui est ATTENDU   : 'Elio_Muxis_V1.rule'") >> test_echec_temp.py
echo if prog1 == "Elio_Muxis_V1.rule": >> test_echec_temp.py
echo     print("   RÉSULTAT : RÉUSSI") >> test_echec_temp.py
echo else: >> test_echec_temp.py
echo     print("   RÉSULTAT : ÉCHOUÉ") >> test_echec_temp.py
echo. >> test_echec_temp.py
echo # Test 3 - SN différent nom vs contenu (comme vos vrais logs) >> test_echec_temp.py
echo print("\nTest 3 - SN différent nom vs contenu") >> test_echec_temp.py
echo print("   Nom fichier : 25.004_SN1000_1310.pdf") >> test_echec_temp.py
echo print("   Contenu PDF : SN03F86-P11278-010-001") >> test_echec_temp.py
echo sn_nom = VerifPdf.GetSnFromString("25.004_SN1000_1310.pdf") >> test_echec_temp.py
echo sn_contenu = "SN03F86-P11278-010-001"  # Votre vrai SN du contenu >> test_echec_temp.py
echo print(f"   Ce qui est TROUVÉ    : SN nom='{sn_nom}' vs SN contenu='{sn_contenu}'") >> test_echec_temp.py
echo print(f"   Ce qui est ATTENDU   : SN identiques") >> test_echec_temp.py
echo if sn_nom == sn_contenu: >> test_echec_temp.py
echo     print("   RÉSULTAT : RÉUSSI") >> test_echec_temp.py
echo else: >> test_echec_temp.py
echo     print("   RÉSULTAT : ÉCHOUÉ - SN différents (comme dans vos logs)") >> test_echec_temp.py
echo. >> test_echec_temp.py
echo # Test 4 - Chercher mauvais programme >> test_echec_temp.py
echo print("\nTest 4 - Mauvais programme attendu") >> test_echec_temp.py
echo print("   Contenu : Rapport avec Elio_Muxis_V1.rule") >> test_echec_temp.py
echo contenu_prog = "Rapport avec Elio_Muxis_V1.rule" >> test_echec_temp.py
echo prog2 = VerifPdf.GetProgFromString(contenu_prog) >> test_echec_temp.py
echo print(f"   Programme détecté : {prog2}") >> test_echec_temp.py
echo print("   Programme attendu : AutreProgramme.rule") >> test_echec_temp.py
echo if prog2 == "AutreProgramme.rule": >> test_echec_temp.py
echo     print("   RÉUSSI") >> test_echec_temp.py
echo else: >> test_echec_temp.py
echo     print("   ÉCHOUÉ") >> test_echec_temp.py
echo. >> test_echec_temp.py
echo # Test 5 - Fichier avec FAIL (non conforme) >> test_echec_temp.py
echo print("\nTest 5 - Fichier avec FAIL") >> test_echec_temp.py
echo print("   Contenu : Résultat test FAIL - non conforme") >> test_echec_temp.py
echo contenu_fail = "Résultat test FAIL - non conforme" >> test_echec_temp.py
echo has_fail = "FAIL" in contenu_fail >> test_echec_temp.py
echo print(f"   FAIL détecté : {has_fail}") >> test_echec_temp.py
echo print("   FAIL attendu : False (pas de FAIL)") >> test_echec_temp.py
echo if not has_fail: >> test_echec_temp.py
echo     print("   RÉUSSI") >> test_echec_temp.py
echo else: >> test_echec_temp.py
echo     print("   ÉCHOUÉ - Fichier non conforme") >> test_echec_temp.py
echo. >> test_echec_temp.py
echo # Test 6 - Format SN impossible >> test_echec_temp.py
echo print("\nTest 6 - Format SN impossible") >> test_echec_temp.py
echo print("   Fichier : image_scan.jpg") >> test_echec_temp.py
echo sn_impossible = VerifPdf.GetSnFromString("image_scan.jpg") >> test_echec_temp.py
echo print(f"   SN détecté : {sn_impossible}") >> test_echec_temp.py
echo print("   SN attendu : SN999") >> test_echec_temp.py
echo if sn_impossible == "SN999": >> test_echec_temp.py
echo     print("   RÉUSSI") >> test_echec_temp.py
echo else: >> test_echec_temp.py
echo     print("   ÉCHOUÉ") >> test_echec_temp.py
echo. >> test_echec_temp.py
echo print("\n" + "=" * 45) >> test_echec_temp.py
echo print("FIN DES TESTS D'ÉCHEC") >> test_echec_temp.py
echo print("Ces échecs correspondent aux vraies erreurs de votre système") >> test_echec_temp.py

REM Lancer le test
python test_echec_temp.py

REM Nettoyer
del test_echec_temp.py

echo.
pause
