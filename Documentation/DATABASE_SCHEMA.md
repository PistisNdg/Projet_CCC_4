# 📊 Schéma de Base de Données - Media Tracking System

## Vue d'ensemble

La base de données SQLite3 contient 4 tables principales pour tracker la visibilité des médias:

```
┌─────────────────┐
│     media       │
├─────────────────┤
│ id (PK)         │
│ media_id (UK)   │
│ title           │
│ type            │
│ url             │
│ created_at      │
└─────────────────┘
        │
        ├─────────────────────────────┐
        │                             │
        ▼                             ▼
┌──────────────────┐        ┌────────────────────┐
│ visibility_event │        │   media_stats      │
├──────────────────┤        ├────────────────────┤
│ id (PK)          │        │ id (PK)            │
│ media_id (FK)    │        │ media_id (FK, UK)  │
│ session_id       │        │ total_views        │
│ event_type       │        │ total_impressions  │
│ visibility_%     │        │ avg_visibility_%   │
│ viewport_width   │        │ total_view_time_ms │
│ viewport_height  │        │ unique_viewers     │
│ device_type      │        │ last_updated       │
│ user_agent       │        └────────────────────┘
│ timestamp        │
│ duration_ms      │
└──────────────────┘
        │
        └──────────────────────┐
                               │
                               ▼
                    ┌──────────────────────┐
                    │   user_session       │
                    ├──────────────────────┤
                    │ id (PK)              │
                    │ session_id (UK)      │
                    │ page_url             │
                    │ ip_address           │
                    │ user_agent           │
                    │ start_time           │
                    │ end_time             │
                    └──────────────────────┘
```

---

## Détails des Tables

### 1. TABLE: media

Stocke les informations sur les médias à tracker.

```sql
CREATE TABLE media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id TEXT UNIQUE NOT NULL,
    title TEXT,
    type TEXT,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Colonnes:**
- `id`: Identifiant unique auto-généré
- `media_id`: Identifiant unique du média (format: `type_number` ex: `img_1`)
- `title`: Titre descriptif du média
- `type`: Type de média (image, video, text)
- `url`: URL de la ressource
- `created_at`: Timestamp de création

**Index:**
- Aucun index spécifique défini (clé primaire)

**Exemple:**
```
id | media_id | title              | type  | url                          | created_at
---+----------+--------------------+-------+------------------------------+------------------
1  | img_1    | Produit Vedette 1  | image | https://example.com/img1.jpg | 2024-04-01 10:00
2  | vid_1    | Tutoriel Produit   | video | https://example.com/vid1.mp4 | 2024-04-01 10:05
```

---

### 2. TABLE: visibility_event

Enregistre chaque événement de visibilité pour un média.

```sql
CREATE TABLE visibility_event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    event_type TEXT,
    visibility_percentage INTEGER,
    viewport_width INTEGER,
    viewport_height INTEGER,
    device_type TEXT,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_ms INTEGER,
    FOREIGN KEY (media_id) REFERENCES media(media_id)
);
```

**Colonnes:**
- `id`: Identifiant unique
- `media_id`: Référence au média (FK)
- `session_id`: Référence à la session utilisateur
- `event_type`: Type d'événement (view, view_complete, impression, click)
- `visibility_percentage`: Pourcentage visible (0-100)
- `viewport_width`: Largeur du viewport en pixels
- `viewport_height`: Hauteur du viewport en pixels
- `device_type`: Type d'appareil (desktop, tablet, mobile)
- `user_agent`: String du navigateur
- `timestamp`: Timestamp de l'événement
- `duration_ms`: Durée de visibilité en millisecondes

**Index:**
- `idx_visibility_media`: Sur media_id pour requêtes rapides
- `idx_visibility_session`: Sur session_id pour filtrer par session
- `idx_visibility_timestamp`: Sur timestamp pour les requêtes temporelles

**Exemple:**
```
id | media_id | session_id | event_type     | visibility_% | viewport_width | device_type | duration_ms
---+----------+------------+----------------+--------------+----------------+-------------+------------
1  | img_1    | uuid-1     | view_complete  | 85           | 1920           | desktop     | 2500
2  | img_1    | uuid-2     | view_complete  | 65           | 768            | tablet      | 1800
3  | vid_1    | uuid-3     | view_complete  | 95           | 1920           | desktop     | 8000
```

---

### 3. TABLE: user_session

Gère les sessions utilisateur pour grouper les événements.

```sql
CREATE TABLE user_session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    page_url TEXT,
    ip_address TEXT,
    user_agent TEXT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP
);
```

**Colonnes:**
- `id`: Identifiant unique
- `session_id`: UUID unique de la session
- `page_url`: URL de la page visitée
- `ip_address`: Adresse IP du visiteur
- `user_agent`: String du navigateur
- `start_time`: Timestamp de début de session
- `end_time`: Timestamp de fin de session (NULL si active)

**Index:**
- `idx_session_timestamp`: Sur start_time pour historique

**Exemple:**
```
id | session_id | page_url                        | ip_address      | start_time           | end_time
---+------------+---------------------------------+-----------------+----------------------+----------------------
1  | uuid-1     | http://localhost/test_page.html | 192.168.1.100   | 2024-04-01 10:00:00 | 2024-04-01 10:15:30
2  | uuid-2     | http://localhost/test_page.html | 192.168.1.101   | 2024-04-01 10:05:00 | NULL
```

---

### 4. TABLE: media_stats

Stocke les statistiques agrégées et mises à jour régulièrement.

```sql
CREATE TABLE media_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id TEXT UNIQUE NOT NULL,
    total_views INTEGER DEFAULT 0,
    total_impressions INTEGER DEFAULT 0,
    average_visibility_percentage REAL DEFAULT 0,
    total_view_time_ms INTEGER DEFAULT 0,
    unique_viewers INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (media_id) REFERENCES media(media_id)
);
```

**Colonnes:**
- `id`: Identifiant unique
- `media_id`: Référence au média (FK, UNIQUE)
- `total_views`: Nombre total de fois où le média a été vu
- `total_impressions`: Total des impressions
- `average_visibility_percentage`: Pourcentage moyen de visibilité
- `total_view_time_ms`: Durée totale d'exposition en ms
- `unique_viewers`: Nombre de visiteurs uniques
- `last_updated`: Timestamp de dernière mise à jour

**Index:**
- Clé primaire et unique sur media_id

**Exemple:**
```
id | media_id | total_views | total_impressions | avg_visibility_% | total_view_time_ms | unique_viewers
---+----------+-------------+-------------------+------------------+--------------------+----------------
1  | img_1    | 150         | 200               | 78.5             | 375000             | 45
2  | vid_1    | 85          | 120               | 92.0             | 680000             | 32
```

---

## Types de Données

| Type SQL      | Utilisation                      | Exemples              |
|---------------|----------------------------------|-----------------------|
| INTEGER       | ID, compteurs, dimensions        | 1, 1920, 85          |
| TEXT          | Chaînes de caractères            | "image", UUID, URLs   |
| REAL          | Nombres décimaux                 | 78.5, 92.0           |
| TIMESTAMP     | Dates et heures                  | CURRENT_TIMESTAMP    |

---

## Requêtes Utiles

### Obtenir les stats d'un média
```sql
SELECT * FROM media_stats WHERE media_id = 'img_1';
```

### Événements par jour pour un média
```sql
SELECT 
    DATE(timestamp) as day,
    COUNT(*) as events,
    AVG(visibility_percentage) as avg_visibility
FROM visibility_event
WHERE media_id = 'img_1'
GROUP BY DATE(timestamp);
```

### Top 5 médias par visibilité
```sql
SELECT media_id, average_visibility_percentage
FROM media_stats
ORDER BY average_visibility_percentage DESC
LIMIT 5;
```

### Sessions actives
```sql
SELECT * FROM user_session WHERE end_time IS NULL;
```

### Temps moyen d'exposition
```sql
SELECT 
    media_id,
    AVG(duration_ms) as avg_duration
FROM visibility_event
GROUP BY media_id;
```

---

## Contraintes d'Intégrité

- **Foreign Keys**: Activées pour garantir la cohérence
- **Unique Constraints**: media_id doit être unique dans media et media_stats
- **Not Null**: Certaines colonnes sont obligatoires
- **Cascade**: Suppression en cascade possible sur demande

---

## Maintenance

### Nettoyage des Anciennes Données
```sql
-- Supprimer les événements de plus de 90 jours
DELETE FROM visibility_event 
WHERE timestamp < datetime('now', '-90 days');

-- Supprimer les sessions fermées depuis plus de 30 jours
DELETE FROM user_session 
WHERE end_time < datetime('now', '-30 days');
```

### Optimization
```sql
-- Analyser et optimiser
VACUUM;
ANALYZE;
```

### Taille de la Base
```sql
-- Vérifier la taille
SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size();
```

---

## Considérations de Performance

1. **Index Pattern**: Les index sur `media_id`, `session_id`, et `timestamp` optimisent les requêtes
2. **Bulk Inserts**: Grouper les événements pour réduire les surcharges
3. **Partitioning**: Considérer de partitionner par date pour très gros volumes
4. **Archivage**: Archiver les données anciennes dans une table séparée si nécessaire

---

**Version du Schéma**: 1.0
**SQLite Version**: 3.x+
**Créée le**: 2024-04-01
