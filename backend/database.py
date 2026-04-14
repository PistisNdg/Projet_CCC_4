import sqlite3
import json
from datetime import datetime
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'media_tracking.db')

def get_connection():
    """Crée une connexion à la base de données SQLite3"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialise la base de données avec les tables nécessaires"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table pour les médias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            media_id TEXT UNIQUE NOT NULL,
            title TEXT,
            type TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table pour les événements de visibilité
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visibility_event (
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
        )
    ''')
    
    # Table pour les sessions utilisateur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_session (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            page_url TEXT,
            ip_address TEXT,
            user_agent TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP
        )
    ''')
    
    # Table pour les statistiques agrégées
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            media_id TEXT UNIQUE NOT NULL,
            total_views INTEGER DEFAULT 0,
            total_impressions INTEGER DEFAULT 0,
            average_visibility_percentage REAL DEFAULT 0,
            total_view_time_ms INTEGER DEFAULT 0,
            unique_viewers INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (media_id) REFERENCES media(media_id)
        )
    ''')
    
    # Créer des indices pour les requêtes fréquentes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_visibility_media ON visibility_event(media_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_visibility_session ON visibility_event(session_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_visibility_timestamp ON visibility_event(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_session_timestamp ON user_session(start_time)')
    
    conn.commit()
    conn.close()
    print("✓ Base de données initialisée avec succès")

if __name__ == '__main__':
    init_database()
