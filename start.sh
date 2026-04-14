#!/bin/bash

# Script de démarrage du système de suivi de visibilité média

echo ""
echo "========================================"
echo "Systeme de Suivi de Visibilite Media"
echo "========================================"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python 3 n'est pas installé"
    exit 1
fi

echo "[OK] Python trouvé: $(python3 --version)"

# Créer un environnement virtuel si n'existe pas
if [ ! -d "venv" ]; then
    echo ""
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
echo ""
echo "Installation des dépendances..."
pip install -q -r backend/requirements.txt

# Initialiser la base de données
echo ""
echo "Initialisation de la base de données..."
python3 backend/database.py

# Démarrer l'API Flask
echo ""
echo "========================================"
echo "Demarrage de l'API Flask..."
echo "========================================"
echo ""
echo "L'API sera disponible sur: http://localhost:5000"
echo "Dashboard:                http://localhost:8000 (après démarrage du serveur web)"
echo ""

python3 backend/app.py
