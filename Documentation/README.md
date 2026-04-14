# 📊 Système de Suivi de Visibilité Média

Un système complet et avancé de suivi de visibilité des médias (images, vidéos, texte) sur une page web. Le système detecte automatiquement quand les médias entrent dans le champ de vision de l'utilisateur, enregistre la durée de visibilité et le pourcentage de visibilité, puis envoie ces données à une API Flask qui les stocke dans une base de données SQLite3.

## 🎯 Caractéristiques Principales

- **Tracking de Visibilité en Temps Réel** : Détecte automatiquement quand un média est visible dans le viewport
- **Suivi Multi-Médias** : Support des images, vidéos et texte
- **API RESTful** : API Flask pour gérer les médias et les événements de tracking
- **Base de Données SQLite3** : Stockage persistant des données de suivi
- **Dashboard Analytique** : Visualisation interactive des statistiques avec graphiques Chart.js
- **Capacité Batch** : Les événements sont groupés par batch avant envoi à l'API
- **Gestion Offline** : Les événements sont mis en queue si la connexion est perdue
- **Responsive** : Design moderne et adaptatif pour desktop et mobile

## 📁 Structure du Projet

```
Projet_CCC/
├── backend/                    # API Flask et base de données
│   ├── app.py                 # Application Flask principale
│   ├── database.py            # Configuration et initialisation SQLite3
│   ├── models.py              # Modèles de données (Media, VisibilityEvent, etc.)
│   └── requirements.txt        # Dépendances Python
├── frontend/                   # Interface web et page de test
│   ├── test_page.html         # Page de test avec médias variés
│   ├── dashboard.html         # Dashboard analytique
│   ├── tracking.js            # Module principal de tracking
│   ├── api.js                 # Client API pour communication
│   └── styles.css             # Styles CSS globaux
└── database/                   # Stockage de la base de données
    └── media_tracking.db      # Base de données SQLite3
```

## 🚀 Installation

### Prérequis

- Python 3.8+
- Un navigateur web moderne (Chrome, Firefox, Safari, Edge)

### Étapes d'Installation

1. **Cloner/Télécharger le projet**
   ```bash
   cd c:\NLP\NLP_Consulting\Programmes\Projet_Python\Projet_CCC
   ```

2. **Créer un environnement virtuel (optionnel mais recommandé)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Sur Windows
   ```

3. **Installer les dépendances Python**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Initialiser la base de données**
   ```bash
   python backend/database.py
   ```

## 🎮 Utilisation

### Démarrer l'API Flask

```bash
python backend/app.py
```

L'API sera disponible sur `http://localhost:5000`

### Ouvrir la Page de Test

Ouvrez `frontend/test_page.html` dans votre navigateur. Vous pouvez :
- Utiliser un serveur local (Python : `python -m http.server` dans le dossier frontend)
- Ou ouvrir directement le fichier HTML

### Accéder au Dashboard

Une fois des données collectées, ouvrez `frontend/dashboard.html` pour visualiser :
- Statistiques globales de visibilité
- Liste des médias avec leurs performances
- Graphiques temporels et de distribution
- Heatmap d'activité
- Comparaison entre les médias

## 📊 Architecture Téchnique

### Backend - API Flask

L'API expose les endpoints suivants :

#### Sessions
- `POST /api/session/create` - Créer une session utilisateur
- `POST /api/session/end/<session_id>` - Terminer une session

#### Tracking
- `POST /api/tracking/record` - Enregistrer un événement de visibilité
- `POST /api/tracking/batch` - Enregistrer plusieurs événements

#### Médias
- `GET /api/media` - Récupérer tous les médias
- `POST /api/media/create` - Créer un nouveau média

#### Statistiques
- `GET /api/stats/all` - Récupérer les stats de tous les médias
- `GET /api/stats/media/<media_id>` - Récupérer les stats d'un média
- `GET /api/stats/media/<media_id>/timeline` - Récupérer la timeline de visibilité

### Base de Données

Tables principales:
- **media** : Stocke les informations des médias
- **visibility_event** : Enregistre chaque événement de visibilité
- **user_session** : Gère les sessions utilisateur
- **media_stats** : Statistiques agrégées par média

### Frontend - Tracking JavaScript

Le module `tracking.js` implement:
- **IntersectionObserver API** : Détecte la visibilité des éléments
- **Batching** : Regroupe les événements avant envoi
- **Offline Support** : Met en queue les événements en cas de perte de connexion
- **Device Detection** : Détecte le type d'appareil (mobile, tablet, desktop)

## 💾 Données Collectées

Pour chaque événement de visibilité, le système enregistre:

```json
{
  "media_id": "img_1",
  "session_id": "uuid",
  "event_type": "view_complete",
  "visibility_percentage": 85,
  "viewport_width": 1920,
  "viewport_height": 1080,
  "device_type": "desktop",
  "user_agent": "Mozilla/5.0...",
  "duration_ms": 2500
}
```

Les statistiques agrégées incluent:
- Nombre total de vues
- Nombre d'impressions
- Pourcentage moyen de visibilité
- Durée totale d'exposition
- Nombre de spectateurs uniques

## 🔧 Configuration

### URLs API
Modifier l'URL de base dans `frontend/tracking.js` et `frontend/api.js`:
```javascript
const tracker = new MediaVisibilityTracker('http://votre-api.com/api');
```

### Taille du Batch
Dans `frontend/tracking.js`:
```javascript
this.batchSize = 10;        // Nombre d'événements par batch
this.batchTimeout = 5000;   // Délai d'attente en ms
```

### Port Flask
Dans `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📈 Cas d'Usage

1. **Analyse de Contenu Web** : Comprendre l'exposition réelle des contenus
2. **Optimisation UX** : Identifier les sections très/peu visibles
3. **Publicité** : Mesurer l'exposition réelle des annonces
4. **Analyse Facebook-like** : Similaire aux statistiques de visibilité de Facebook
5. **A/B Testing** : Comparer la visibilité de différentes mises en page

## 🛠️ Technologies Utilisées

### Backend
- **Flask** : Framework web Python
- **SQLite3** : Base de données légère et portable
- **CORS** : Support des requêtes cross-origin

### Frontend
- **HTML5** : Structure sémantique
- **CSS3** : Design moderne et responsive
- **JavaScript ES6+** : Logique de tracking
- **Chart.js** : Visualisation de données
- **Intersection Observer API** : Détection de visibilité

## 📝 Exemples d'Utilisation

### Créer un Média
```javascript
await api.createMedia('img_1', 'Mon Image', 'image', 'https://...');
```

### Tracker un Élément
```javascript
const element = document.getElementById('my-image');
tracker.trackElement(element, 'img_1', 'image', { title: 'Mon Image' });
```

### Récupérer les Stats
```javascript
const stats = await api.getAllStats();
console.log(stats);
```

## 🐛 Dépannage

**Problem**: L'API ne démarre pas
- Solution : Vérifier que le port 5000 est libre, ou modifier le port dans `app.py`

**Problem**: Les données ne sont pas envoyées
- Solution : Vérifier la console du navigateur (F12) pour les erreurs CORS ou réseau

**Problem**: Le dashboard ne charge pas les données
- Solution : Vérifier que l'API Flask est démarrée et accessible à `http://localhost:5000/api`

## 📚 Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- [Chart.js Documentation](https://www.chartjs.org/)
- [SQLite3 Documentation](https://www.sqlite.org/docs.html)

## 📄 Licence

Ce projet est fourni à titre d'exemple éducatif.

## 👤 Auteur

Développé comme un système complet de suivi de visibilité média.

---

**Version**: 1.0.0  
**Date**: 2024  
**Statut**: Production Ready ✅
