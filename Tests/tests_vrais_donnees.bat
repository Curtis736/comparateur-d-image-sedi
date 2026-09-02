@echo off
cd /d "%~dp0"
echo TESTS AVEC VOS VRAIES DONNÉES
echo =============================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR - Python non trouvé
    pause
    exit /b 1
)

REM Créer le test directement dans le .bat
echo import sys > test_temp.py
echo import os >> test_temp.py
echo sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")) >> test_temp.py
echo. >> test_temp.py
echo try: >> test_temp.py
echo     import VerifPdf >> test_temp.py
echo     import VerifPdfRoutine >> test_temp.py
echo except ImportError as e: >> test_temp.py
echo     print(f"ERREUR - Import : {e}") >> test_temp.py
echo     exit(1) >> test_temp.py
echo. >> test_temp.py
echo print("TESTS AVEC VOS VRAIES DONNÉES") >> test_temp.py
echo print("=" * 35) >> test_temp.py
echo. >> test_temp.py
echo # Test 1 - Fichier 25.004_SN1000_1310.pdf >> test_temp.py
echo print("\nTest 1 - Fichier 25.004_SN1000_1310.pdf") >> test_temp.py
echo sn1 = VerifPdf.GetSnFromString("25.004_SN1000_1310.pdf") >> test_temp.py
echo print(f"   Ce qui est TROUVÉ    : '{sn1}'") >> test_temp.py
echo print(f"   Ce qui est ATTENDU   : '1000_1310'") >> test_temp.py
echo if sn1 == "1000_1310": >> test_temp.py
echo     print("   RÉSULTAT : RÉUSSI") >> test_temp.py
echo else: >> test_temp.py
echo     print("   RÉSULTAT : ÉCHOUÉ") >> test_temp.py
echo. >> test_temp.py
echo # Test 2 - Fichier 25.004_SN1004_1310.pdf >> test_temp.py
echo print("\nTest 2 - Fichier 25.004_SN1004_1310.pdf") >> test_temp.py
echo sn2 = VerifPdf.GetSnFromString("25.004_SN1004_1310.pdf") >> test_temp.py
echo print(f"   Ce qui est TROUVÉ    : '{sn2}'") >> test_temp.py
echo print(f"   Ce qui est ATTENDU   : '1004_1310'") >> test_temp.py
echo if sn2 == "1004_1310": >> test_temp.py
echo     print("   RÉSULTAT : RÉUSSI") >> test_temp.py
echo else: >> test_temp.py
echo     print("   RÉSULTAT : ÉCHOUÉ") >> test_temp.py
echo. >> test_temp.py
echo # Test 3 - Fichier 23.270D SN 240 1310.pdf >> test_temp.py
echo print("\nTest 3 - Fichier 23.270D SN 240 1310.pdf") >> test_temp.py
echo sn3 = VerifPdf.GetSnFromString("23.270D SN 240 1310.pdf") >> test_temp.py
echo print(f"   Ce qui est TROUVÉ    : '{sn3}'") >> test_temp.py
echo print(f"   Ce qui est ATTENDU   : '240'") >> test_temp.py
echo if sn3 == "240": >> test_temp.py
echo     print("   RÉSULTAT : RÉUSSI") >> test_temp.py
echo else: >> test_temp.py
echo     print("   RÉSULTAT : ÉCHOUÉ") >> test_temp.py
echo. >> test_temp.py
echo # Test 4 - Programme Elio_Muxis_V1.rule >> test_temp.py
echo print("\nTest 4 - Programme Elio_Muxis_V1.rule") >> test_temp.py
echo contenu = "Rapport SN03F86-P11278-010-001 avec Elio_Muxis_V1.rule validé" >> test_temp.py
echo prog = VerifPdf.GetProgFromString(contenu) >> test_temp.py
echo print(f"   Ce qui est TROUVÉ    : '{prog}'") >> test_temp.py
echo print(f"   Ce qui est ATTENDU   : 'Elio_Muxis_V1.rule'") >> test_temp.py
echo if prog == "Elio_Muxis_V1.rule": >> test_temp.py
echo     print("   RÉSULTAT : RÉUSSI") >> test_temp.py
echo else: >> test_temp.py
echo     print("   RÉSULTAT : ÉCHOUÉ") >> test_temp.py
echo. >> test_temp.py
echo # Test 5 - Normalisation SN41_SE >> test_temp.py
echo print("\nTest 5 - Normalisation SN41_SE") >> test_temp.py
echo sn_norm = VerifPdfRoutine._normalize_sn("SN41_SE") >> test_temp.py
echo print(f"   Ce qui est TROUVÉ    : '{sn_norm}'") >> test_temp.py
echo print(f"   Ce qui est ATTENDU   : 'SN41'") >> test_temp.py
echo if sn_norm == "SN41": >> test_temp.py
echo     print("   RÉSULTAT : RÉUSSI") >> test_temp.py
echo else: >> test_temp.py
echo     print("   RÉSULTAT : ÉCHOUÉ") >> test_temp.py
echo. >> test_temp.py
echo # Test 6 - Normalisation Elio_Muxis_V1.rule >> test_temp.py
echo print("\nTest 6 - Normalisation Elio_Muxis_V1.rule") >> test_temp.py
echo prog_norm = VerifPdfRoutine._normalize_program_name("Elio_Muxis_V1.rule") >> test_temp.py
echo print(f"   Ce qui est TROUVÉ    : '{prog_norm}'") >> test_temp.py
echo print(f"   Ce qui est ATTENDU   : 'elio_muxis_v1'") >> test_temp.py
echo if prog_norm == "elio_muxis_v1": >> test_temp.py
echo     print("   RÉSULTAT : RÉUSSI") >> test_temp.py
echo else: >> test_temp.py
echo     print("   RÉSULTAT : ÉCHOUÉ") >> test_temp.py
echo. >> test_temp.py
echo print("\n" + "=" * 35) >> test_temp.py
echo print("FIN DES TESTS") >> test_temp.py

REM Lancer le test
python test_temp.py

REM Nettoyer
del test_temp.py

echo.
pause
