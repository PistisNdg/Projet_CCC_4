# API Documentation - Media Tracking System

## 📡 Endpoints API

### Base URL
```
http://localhost:5000/api
```

---

## 👤 Session Management Endpoints

### 1. Create Session
**POST** `/session/create`

Crée une nouvelle session utilisateur.

**Request Body:**
```json
{
  "page_url": "http://example.com/page"
}
```

**Response (201):**
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Session créée avec succès"
}
```

### 2. End Session
**POST** `/session/end/<session_id>`

Termine une session utilisateur.

**Response (200):**
```json
{
  "success": true,
  "message": "Session terminée avec succès"
}
```

---

## 📹 Visibility Tracking Endpoints

### 3. Record Single Event
**POST** `/tracking/record`

Enregistre un seul événement de visibilité.

**Request Body:**
```json
{
  "media_id": "img_1",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "view_complete",
  "visibility_percentage": 85,
  "viewport_width": 1920,
  "viewport_height": 1080,
  "device_type": "desktop",
  "user_agent": "Mozilla/5.0...",
  "duration_ms": 2500
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Événement enregistré avec succès"
}
```

### 4. Record Batch Events
**POST** `/tracking/batch`

Enregistre plusieurs événements en batch pour plus d'efficacité.

**Request Body:**
```json
{
  "events": [
    {
      "media_id": "img_1",
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "event_type": "view_complete",
      "visibility_percentage": 75,
      "duration_ms": 2000
    },
    {
      "media_id": "vid_1",
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "event_type": "view_complete",
      "visibility_percentage": 50,
      "duration_ms": 5000
    }
  ]
}
```

**Response (201):**
```json
{
  "success": true,
  "processed": 2,
  "total": 2,
  "message": "2/2 événements enregistrés"
}
```

---

## 📷 Media Management Endpoints

### 5. Get All Media
**GET** `/media`

Récupère la liste de tous les médias.

**Response (200):**
```json
{
  "success": true,
  "media": [
    {
      "id": 1,
      "media_id": "img_1",
      "title": "Produit Vedette 1",
      "type": "image",
      "url": "https://example.com/img1.jpg",
      "created_at": "2024-04-01T10:30:00"
    }
  ]
}
```

### 6. Create Media
**POST** `/media/create`

Crée une nouvelle entrée média.

**Request Body:**
```json
{
  "media_id": "img_1",
  "title": "Produit Vedette",
  "type": "image",
  "url": "https://example.com/image.jpg"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Média créé avec succès"
}
```

---

## 📊 Analytics & Statistics Endpoints

### 7. Get All Stats
**GET** `/stats/all`

Récupère les statistiques agrégées de tous les médias.

**Response (200):**
```json
{
  "success": true,
  "stats": [
    {
      "id": 1,
      "media_id": "img_1",
      "total_views": 150,
      "total_impressions": 200,
      "average_visibility_percentage": 78,
      "total_view_time_ms": 375000,
      "unique_viewers": 45,
      "last_updated": "2024-04-01T15:45:00"
    }
  ],
  "total_media": 10
}
```

### 8. Get Specific Media Stats
**GET** `/stats/media/<media_id>`

Récupère les statistiques pour un média spécifique.

**Response (200):**
```json
{
  "success": true,
  "stats": {
    "id": 1,
    "media_id": "img_1",
    "total_views": 150,
    "total_impressions": 200,
    "average_visibility_percentage": 78,
    "total_view_time_ms": 375000,
    "unique_viewers": 45,
    "last_updated": "2024-04-01T15:45:00"
  },
  "events_count": 523
}
```

### 9. Get Visibility Timeline
**GET** `/stats/media/<media_id>/timeline`

Récupère la timeline horaire de visibilité pour un média.

**Response (200):**
```json
{
  "success": true,
  "media_id": "img_1",
  "timeline": {
    "2024-04-01 10": {
      "count": 25,
      "avg_visibility": 2500,
      "total_duration": 62500
    },
    "2024-04-01 11": {
      "count": 42,
      "avg_visibility": 1785,
      "total_duration": 74970
    }
  }
}
```

---

## 🏥 Health Check Endpoint

### 10. Health Check
**GET** `/health`

Vérifie que l'API est opérationnelle.

**Response (200):**
```json
{
  "success": true,
  "status": "API Media Tracking est opérationnelle",
  "timestamp": "2024-04-01T15:45:30.123456"
}
```

---

## 📋 Parameters Reference

### Media Types
- `image` - Images statiques
- `video` - Contenus vidéo
- `text` - Contenu texte

### Event Types
- `view` - Visualisation (entrée dans le viewport)
- `view_complete` - Fin de visualisation
- `impression` - Impression
- `click` - Clic sur le média

### Device Types
- `desktop` - Ordinateur de bureau
- `tablet` - Tablette
- `mobile` - Téléphone mobile

### HTTP Status Codes
- `200` - OK - Requête réussie
- `201` - Created - Ressource créée
- `400` - Bad Request - Données invalides
- `404` - Not Found - Ressource non trouvée
- `500` - Internal Server Error - Erreur serveur

---

## 🔄 Common Response Format

### Success Response
```json
{
  "success": true,
  "data": {},
  "message": "Description"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Description de l'erreur"
}
```

---

## 🔐 CORS Headers

L'API accepte les requêtes CORS de toutes les origines. Headers supportés:
- `Content-Type: application/json`
- `Accept: application/json`

---

## 📈 Data Collection Best Practices

1. **Batch Events** - Envoyer les événements par batch plutôt qu'un par un
2. **Monitor Connection** - Gérer les déconnexions et remettre en queue
3. **Rate Limiting** - Respecter les délais entre les envois
4. **Session Management** - Toujours terminer les sessions correctement
5. **Error Handling** - Implémenter la gestion des erreurs réseau

---

## 🧪 Testing with cURL

### Créer une Session
```bash
curl -X POST http://localhost:5000/api/session/create \
  -H "Content-Type: application/json" \
  -d '{"page_url": "http://example.com"}'
```

### Enregistrer un Événement
```bash
curl -X POST http://localhost:5000/api/tracking/record \
  -H "Content-Type: application/json" \
  -d '{
    "media_id": "img_1",
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "event_type": "view_complete",
    "visibility_percentage": 85,
    "duration_ms": 2500
  }'
```

### Récupérer les Stats
```bash
curl http://localhost:5000/api/stats/all
```

---

## 📝 Notes

- Toutes les timestamps sont en UTC ISO 8601 format
- Les durées sont en millisecondes (ms)
- Les pourcentages de visibilité vont de 0 à 100
- Les IDs de session sont des UUIDs v4
- La base de données est SQLite3 stockée localement

---

**Version de l'API**: 1.0.0
**Dernière mise à jour**: 2024-04-01
