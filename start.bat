@echo off
REM Script de démarrage du système de suivi de visibilité média

echo.
echo ========================================
echo Systeme de Suivi de Visibilite Media
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Python n'est pas installé ou non accessible
    pause
    exit /b 1
)

echo [OK] Python trouvé

REM Créer un environnement virtuel si n'existe pas
if not exist "venv" (
    echo.
    echo Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Installer les dépendances
echo.
echo Installation des dépendances...
pip install -q -r backend/requirements.txt

REM Initialiser la base de données
echo.
echo Initialisation de la base de données...
python backend/database.py

REM Démarrer l'API Flask
echo.
echo ========================================
echo Demarrage de l'API Flask...
echo ========================================
echo.
echo L'API sera disponible sur: http://localhost:5000
echo Dashboard:                http://localhost:8000 (après démarrage du serveur web)
echo.
python backend/app.py

pause
