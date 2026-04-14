# 🏗️ Architecture Technique du Système

**Projet N°4 - Système de Mesure de Visibilité**  
Niveau 1 - Prototype Fonctionnel

## 📐 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                      NAVIGATEUR CLIENT                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  test_page.html (Facebook-style feed)                │  │
│  │  - 8 publications avec images                         │  │
│  │  - Contenu à tracker                                 │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  tracking.js (Intersection Observer)                 │  │
│  │  - Détecte visibilité                                │  │
│  │  - Mesure pourcentage                                │  │
│  │  - Batch des événements                              │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  api.js (Communication HTTP)                         │  │
│  │  - Envoie événements au serveur                      │  │
│  │  - Récupère statistiques                             │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  dashboard.html (Analytics)                          │  │
│  │  - Affiche grille de publications                   │  │
│  │  - Panel détails avec statistiques                  │  │
│  │  - 3 graphiques Chart.js                            │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↕ HTTP REST
┌─────────────────────────────────────────────────────────────┐
│                    SERVEUR (Python/Flask)                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  app.py - Routes API                                 │  │
│  │  POST /api/session/create                            │  │
│  │  POST /api/session/end/<id>                          │  │
│  │  POST /api/media/create                              │  │
│  │  POST /api/tracking/batch                            │  │
│  │  GET  /api/stats/all                                 │  │
│  │  GET  /api/stats/media/<id>                          │  │
│  │  GET  /api/stats/media/<id>/timeline                 │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  models.py - Modèles de données                      │  │
│  │  - Media.create(), .get_all()                        │  │
│  │  - VisibilityEvent.record(), .get_by_media()        │  │
│  │  - UserSession.create(), .end_session()             │  │
│  │  - MediaStats.update_stats(), .get_all_stats()      │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  database.py - Gestion SQLite                        │  │
│  │  - Connexions                                        │  │
│  │  - Initialisation schéma                             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↕ SQL
┌─────────────────────────────────────────────────────────────┐
│                    BASE DE DONNÉES (SQLite3)                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  media                                               │  │
│  │  - media_id (PK)                                     │  │
│  │  - title, type, url                                 │  │
│  │  - created_at                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  user_session                                        │  │
│  │  - session_id (PK)                                  │  │
│  │  - page_url, user_agent                             │  │
│  │  - start_time, end_time                             │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  visibility_event                                    │  │
│  │  - id (PK)                                          │  │
│  │  - media_id (FK), session_id (FK)                   │  │
│  │  - event_type, visibility_percentage                │  │
│  │  - duration_ms, viewport_width/height               │  │
│  │  - device_type, timestamp                           │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  media_stats                                         │  │
│  │  - media_id (PK)                                    │  │
│  │  - total_views, unique_viewers                      │  │
│  │  - average_visibility_percentage                    │  │
│  │  - total_view_time_ms                               │  │
│  │  - last_updated                                     │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Flux de Données Détaillé

### 1️⃣ Initialisation
```
1. Utilisateur ouvre test_page.html
2. tracker.js crée une session (POST /api/session/create)
3. trackElement() enregistre chaque <img> avec media_id
4. Intersection Observer démarre
```

### 2️⃣ Détection de Visibilité
```
1. Utilisateur scrolle la page
2. Intersection Observer détecte changement de visibilité
3. handleVisibilityChange() mesure pourcentage
4. Événement créé quand contenu devient visible/invisible
```

### 3️⃣ Batching et Envoi
```
1. Événement ajouté à eventBatch[]
2. Chaque 3 secondes: rapport périodique d'activité
3. Quand batch.length >= 10: flushBatch()
4. POST /api/tracking/batch envoie les 10 événements
```

### 4️⃣ Enregistrement BD
```
1. Serveur reçoit POST /api/tracking/batch
2. Pour chaque événement:
   - VisibilityEvent.record() insère en BD
   - MediaStats.update_stats() recalcule statistiques
3. Statistiques agrégées stored en media_stats
```

### 5️⃣ Visualisation
```
1. Utilisateur ouvre dashboard.html
2. loadDashboard() récupère GET /api/stats/all
3. displayPublications() affiche grille
4. Clic sur publication → selectMedia()
5. Récupère stats + timeline + crée 3 graphiques
```

## 🔐 Composants Clés

### Frontend

**tracking.js**
- `MediaVisibilityTracker` classe
- Gère Intersection Observer
- Batch automatique d'événements (10 ou 5s)
- Rapport périodique toutes les 3s

**api.js**
- `MediaAPI` classe
- Communication REST avec serveur
- Endpoints pour sessions, media, tracking, stats

**test_page.html**
- Facebook-style feed layout
- 8 publications avec images réelles
- Composer card (UI Facebook)
- Post cards avec métadonnées

**dashboard.html**
- Grille de publications (gauche)
- Detail panel (droite) avec:
  - Image et informations
  - 6 statistiques de base
  - 4 tiers d'engagement
  - 3 graphiques Chart.js

### Backend

**app.py**
- Flask server sur port 5000
- 8 routes principales
- CORS enabled pour cross-origin
- JSON responses

**models.py**
- 4 classes de données
- Méthodes CRUD simples
- Calculs de statistiques

**database.py**
- Gestion SQLite
- Création schéma automatique
- Connection pooling

## 📊 Statistiques Calculées

```
Par Publication:
- total_views: COUNT(events)
- unique_viewers: COUNT(DISTINCT session_id)
- average_visibility_percentage: AVG(visibility_percentage)
- total_view_time_ms: SUM(duration_ms)
- total_impressions: COUNT(events)

Agrégations:
- Durée moyenne par vue
- Timeline d'activité (par heure)
- Distribution de visibilité (4 tiers)
- Top publications par vues
```

## ⚙️ Configuration

**Serveur:**
- Host: 0.0.0.0
- Port: 5000
- Debug: True (développement)

**BD:**
- Type: SQLite3
- Localisation: /database/media_tracking.db
- Indices: media_id, session_id, timestamp

**Frontend:**
- API Base URL: http://localhost:5000/api
- Batch Size: 10 événements
- Batch Timeout: 5 secondes
- Periodic Report: 3 secondes
- Intersection Threshold: [0, 0.25, 0.5, 0.75, 1.0]

## 🚦 États du Système

```
┌─ Session Créée
│   └─ Medias Trackés
│       └─ Événements Collectés
│           └─ Batch Plein
│               └─ Envoi API
│                   └─ BD Mise à Jour
│                       └─ Stats Calculées
│                           └─ Dashboard Rafraîchi
└─ Session Fermée
    └─ Batch Flush + Session End
```

## 🔗 Dépendances Inter-composants

```
test_page.html
    ├─ tracking.js (détection)
    ├─ api.js (communication)
    └─ styles.css (visual)

dashboard.html
    ├─ api.js (récupération stats)
    ├─ chart.js (visualisation)
    └─ styles.css (visual)

Backend (app.py)
    ├─ models.py (données)
    └─ database.py (persistance)
        └─ media_tracking.db
```

## 🎯 Points de Décision Techniques

1. **Intersection Observer** - Précis, natif, efficace
2. **Batching** - Réduit charge serveur
3. **SQLite3** - Simple, aucune dépendance externe
4. **REST API** - Standard, stateless
5. **Chart.js** - Léger, responsive
