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