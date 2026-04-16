# Quick Start Guide - Media Visibility Tracking

Démarrage rapide du système de suivi de visibilité média en 5 minutes!

## Prérequis

- Python 3.8+ installé
- Git (optionnel)
- Un navigateur web moderne

## Démarrage Rapide (5 min)

### Étape 1: Installer les Dépendances
```bash
# Naviguer dans le dossier du projet
cd Projet_CCC_4/start.

# Installer les dépendances Python
pip install -r Documentation/requirements.txt
```

### Étape 2: Initialiser la Base de Données
```bash
# Initialiser SQLite3 (en cas de besoin mais il est déjà initialisé)
python backend/database.py
```

Vous devriez voir: `✓ Base de données initialisée avec succès`

### Étape 3: Démarrer l'API Flask
```bash
# Lancer l'API
python backend/app.py
```

Vous devriez voir quelque chose comme:
```
 * Serving Flask app 'app'
 * Running on http://0.0.0.0:5000
```


### Étape 4: Ouvrir les Pages Web

#### Option A: Serveur Local Python
```bash
# Dans le dossier frontend, avec un nouveau terminal
cd frontend
python -m http.server 8000
```

Puis ouvrir:
- **Test Page**: http://localhost:8000/test_page.html
- **Dashboard**: http://localhost:8000/dashboard.html

#### Option B: Ouvrir Directement
Double-cliquer sur les fichiers HTML:
- `frontend/test_page.html` (pour tracker les médias)
- `frontend/dashboard.html` (pour voir les statistiques)

## 🔍 Vérifier que Tout Fonctionne

### Test 1: L'API Est-elle Active?
```bash
# Windows
curl http://localhost:5000/api/health

# Mac/Linux
curl -s http://localhost:5000/api | python -m json.tool
```

Vous devriez voir:
```json
{
  "success": true,
  "status": "API Media Tracking est opérationnelle"
}
```

### Test 2: Les Médias Sont-ils Créés?
Visiter: http://localhost:5000/api/media

Devrait retourner une liste vide `[]` au démarrage.

### Test 3: Tracker Fonctionne-t-il?
1. Ouvrir `test_page.html`
2. Ouvrir Console du Navigateur (F12)
3. Scroller la page
4. Vous devriez voir des logs comme `✓ Tracking configuré pour: img_1`

## 📊 Utiliser le Dashboard

1. Ouvrir `test_page.html` et scroller quelques minutes
2. Ouvrir `dashboard.html` dans un autre onglet
3. Vous devriez voir des graphiques et des statistiques!

## 🛠️ Commandes Utiles

|                      Commande                 |             Description          |
|-----------------------------------------------|----------------------------------|
| `python backend/database.py`                  | Réinitialiser la base de données |
| `python generate_test_data.py`                | Générer des données de test      |
| `python generate_test_data.py --sessions 100` | 100 sessions                     |
| `python generate_test_data.py --media 20`     | 20 médias                        |
| `python -m http.server 8000` (dans frontend/) | Serveur web local                |

## 🐛 Troubleshooting

### "Port 5000 Already in Use"
```bash
# Changer le port dans backend/app.py ligne 143:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### "Module not found: Flask"
```bash
# Réinstaller les dépendances
pip install --upgrade -r backend/requirements.txt
```

### "Database is locked"
```bash
# Supprimer le fichier de base de données et le recréer
del database/media_tracking.db
python backend/database.py
```

### "Cannot connect to http://localhost:5000"
```bash
# Vérifier que Flask est démarré (regarder le terminal)
# Si démarré, attendre 2-3 secondes avant de réessayer
```

## 📁 Structure des Fichiers

```
Projet_CCC/
├── backend/
│   ├── app.py              ← Démarrer l'API ici
│   ├── database.py         ← Initialiser la DB ici
│   ├── models.py           ← Modèles de données
│   └── requirements.txt     ← Dépendances
├── frontend/
│   ├── test_page.html      ← Ouvrir pour tracker
│   ├── dashboard.html      ← Ouvrir pour stats
│   ├── tracking.js         ← Module de tracking
│   ├── api.js              ← Client API
│   └── styles.css          ← Styles
├── database/
│   └── media_tracking.db   ← Base de données
├── generate_test_data.py   ← Générer des données
├── start.bat               ← Démarrage Windows
├── start.sh                ← Démarrage Mac/Linux
└── README.md               ← Documentation complète
```

## 📚 Prochaines Étapes

1. **Comprendre le Tracking**: Lire [tracking.js](frontend/tracking.js) - le cœur du système
2. **Explorer les Données**: Lister les tables SQLite avec `sqlite3 database/media_tracking.db`
3. **Modifier les Données**: Éditer `test_page.html` pour ajouter vos propres médias
4. **Déployer**: Voir [README.md](README.md) pour le déploiement en production

## 💡 Conseils

1. **Pour Développer**: Garder la console F12 ouverte pour voir les logs
2. **Pour Tester**: Utiliser le script `generate_test_data.py` pour avoir des données rapidement
3. **Pour Déboguer**: Modifier `FLASK_DEBUG = True` pour le mode debug

## ❓ Questions Fréquentes

**Q: Comment ajouter plus de médias à tracker ?**
A: Modifier `test_page.html` et ajouter des divs avec `id` uniques, puis appeler `tracker.trackElement()`

**Q: Comment exporter les données ?**
A: Les données sont stockées en SQLite3, utiliser un outil SQLite3 ou écrire une route API personnalisée

**Q: Puis-je utiliser cela en production ?**
A: Oui! Voir [README.md](README.md) pour les considérations de production

## 🎯 Prochaine Session

La prochaine fois que vous voulez utiliser le système:

**Windows**: Cliquer sur `start.bat`
**Mac/Linux**: Exécuter `bash start.sh`

Puis ouvrir les fichiers HTML dans votre navigateur.

---

**Besoin d'aide ?** Voir [README.md](README.md) pour la documentation complète.

**Version**: 1.0.0
**Créé**: 2024-04-01