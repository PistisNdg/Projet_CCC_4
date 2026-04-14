# 📋 Guide d'Installation et d'Exécution

**Projet N°4 - Système de Mesure de Visibilité**  
Niveau 1 - Prototype Fonctionnel

## ⚙️ Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Navigateur moderne (Chrome, Firefox, Safari, Edge)
- 100 MB d'espace disque minimum

## 📦 Installation Complète

### Étape 1: Télécharger/Cloner le Projet

```bash
cd /path/to/workspace
# ou le projet existe déjà dans Projet_CCC/
```

### Étape 2: Installer les Dépendances Python

```bash
cd backend
pip install -r requirements.txt
```

**Fichier requirements.txt contient:**
```
Flask==2.3.0
Flask-Cors==4.0.0
```

### Étape 3: Initialiser la Base de Données

```bash
cd backend
python -c "from database import init_database; init_database()"
```

Cela crée `database/media_tracking.db` avec les tables:
- media
- user_session
- visibility_event
- media_stats

### Étape 4: Démarrer le Serveur

```bash
cd backend
python app.py
```

**Résultat attendu:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Étape 5: Accéder aux Pages

Dans un navigateur, ouvrez:

1. **Page de Test:** http://localhost:5000/frontend/test_page.html
   - Affiche 8 publications en Facebook-style feed
   - Les images sont trackées automatiquement
   - Consultez les publications pour générer des événements

2. **Dashboard:** http://localhost:5000/frontend/dashboard.html
   - Affiche la grille des publications
   - Cliquez sur une publication pour voir les statistiques
   - Graphiques affichent la comparaison jour/jour

## 🚀 Démarrage Rapide (Scripts Fournis)

### Sur Windows:
```bash
start.bat
```

### Sur Linux/Mac:
```bash
bash start.sh
```

Ces scripts font:
1. Activent l'env Python (s'il existe)
2. Installent les dépendances
3. Initialisent la BD
4. Démarrent le serveur

## 📁 Structure de Répertoires

```
Projet_CCC/
├── backend/
│   ├── app.py              ← Serveur Flask
│   ├── models.py           ← Modèles de données
│   ├── database.py         ← Gestion SQLite
│   └── requirements.txt    ← Dépendances
├── frontend/
│   ├── test_page.html      ← Page test
│   ├── dashboard.html      ← Dashboard
│   ├── tracking.js         ← Module tracking
│   ├── api.js              ← Module API
│   ├── styles.css          ← Styling
│   └── Images_utilisable/  ← Images (8 fichiers)
├── database/
│   └── media_tracking.db   ← Base SQLite (créée)
├── README.md
├── ARCHITECTURE.md
├── DATABASE_SCHEMA.md
├── INSTALL_GUIDE.md
├── TESTS_REPORT.md
├── start.bat
├── start.sh
└── generate_test_data.py
```

## 🔧 Configuration

### Port du Serveur

Par défaut: **5000**

Pour changer, éditez `backend/app.py` dernière ligne:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Remplacer 5000 par 5001
```

### Chemins des Images

Les images doivent être dans `frontend/Images_utilisable/`

Format supporté: JPG, PNG, GIF

Utilisés dans `test_page.html`:
```javascript
image: 'Images_utilisable/_9fb91bd6-e1ff-4943-a7c5-70af22d3e01a.jpeg'
```

## 🧪 Tester le Système

### Test 1: Sessions
```bash
curl -X POST http://localhost:5000/api/session/create \
  -H "Content-Type: application/json" \
  -d '{"page_url": "http://localhost:5000/frontend/test_page.html"}'
```

### Test 2: Créer un Media
```bash
curl -X POST http://localhost:5000/api/media/create \
  -H "Content-Type: application/json" \
  -d '{
    "media_id": "test_1",
    "title": "Test Media",
    "type": "image",
    "url": "Images_utilisable/test.jpg"
  }'
```

### Test 3: Envoyer un Événement
```bash
curl -X POST http://localhost:5000/api/tracking/batch \
  -H "Content-Type: application/json" \
  -d '{
    "events": [{
      "media_id": "test_1",
      "session_id": "session-123",
      "event_type": "view_complete",
      "visibility_percentage": 85,
      "duration_ms": 3000,
      "device_type": "desktop"
    }]
  }'
```

### Test 4: Récupérer les Stats
```bash
curl http://localhost:5000/api/stats/all
```

## 🐛 Dépannage

### Erreur: "Address already in use"
Port 5000 déjà utilisé. Changez le port dans app.py.

```bash
# Trouver quoi utilise le port 5000
# Windows:
netstat -ano | findstr :5000
# Mac/Linux:
lsof -i :5000
```

### Erreur: "Module not found: Flask"
Installez les dépendances:
```bash
pip install -r backend/requirements.txt
```

### Erreur: "Database connection failed"
Vérifiez que le dossier `database/` existe:
```bash
mkdir -p database
```

Puis réinitialisez:
```bash
python backend/database.py
```

### Les images sont 404
Vérifiez le chemin `frontend/Images_utilisable/` existe avec les fichiers.

### Le tracker ne fonctionne pas
Ouvrez F12 (console dev) et vérifiez:
1. Pas d'erreur JS
2. Les requêtes API vont à `http://localhost:5000/api/...`
3. Les réponses status 201 (créé) ou 200 (OK)

## 📊 Générer des Données de Test

Un script `generate_test_data.py` peut créer de fausses données:

```bash
python generate_test_data.py
```

Cela:
1. Crée 5 sessions
2. Crée 20 événements par session
3. Calcule automatiquement les stats

Puis vérifiez dans le dashboard.

## 🔒 Arrêter le Serveur

Terminal:
```bash
Ctrl+C
```

Le serveur s'arrête gracieusement. La BD est fermée proprement.

## 📈 Monitoring

Pour voir les logs en temps réel:

```bash
# Terminal 1: Serveur
cd backend
python app.py > server.log 2>&1

# Terminal 2: Watch logs
tail -f server.log
```

## 🌐 Accès Distant

Pour accéder depuis une autre machine:

1. Trouvez l'IP locale:
```bash
# Windows:
ipconfig
# Mac/Linux:
ifconfig
```

2. Remplacez `localhost` par l'IP:
```
http://192.168.1.100:5000/frontend/test_page.html
```

3. Assurez le firewall autorise le port 5000.

## ✅ Vérification Installation

Tous les points verts = Installation complète:

- [ ] Python 3.8+ installé
- [ ] Dépendances installées (`pip list` contient Flask)
- [ ] Base de données créée (`database/media_tracking.db` existe)
- [ ] Serveur démarre sans erreur
- [ ] http://localhost:5000/frontend/test_page.html charge
- [ ] http://localhost:5000/frontend/dashboard.html charge
- [ ] Console navigateur sans erreur JS
- [ ] Événements dans les logs serveur

## 📞 Support

**Problème courant:** Erreur CORS
→ Les réponses GET doivent passer Flask-Cors:
```python
from flask_cors import CORS
CORS(app)
```
