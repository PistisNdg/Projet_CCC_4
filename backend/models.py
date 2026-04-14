from datetime import datetime
from database import get_connection
import uuid

class Media:
    """Modèle pour les médias (images, vidéos, texte)"""
    
    @staticmethod
    def create(media_id, title, media_type, url):
        """Crée une nouvelle entrée média"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO media (media_id, title, type, url)
                VALUES (?, ?, ?, ?)
            ''', (media_id, title, media_type, url))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la création du média: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def get_all():
        """Récupère tous les médias"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM media ORDER BY created_at DESC')
        media = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return media


class VisibilityEvent:
    """Modèle pour les événements de visibilité"""
    
    @staticmethod
    def record(media_id, session_id, event_data):
        """Enregistre un événement de visibilité"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO visibility_event 
                (media_id, session_id, event_type, visibility_percentage, 
                 viewport_width, viewport_height, device_type, user_agent, duration_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                media_id,
                session_id,
                event_data.get('event_type', 'view'),
                event_data.get('visibility_percentage', 0),
                event_data.get('viewport_width'),
                event_data.get('viewport_height'),
                event_data.get('device_type'),
                event_data.get('user_agent'),
                event_data.get('duration_ms', 0)
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de l'enregistrement: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def get_by_media(media_id):
        """Récupère tous les événements pour un média"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM visibility_event 
            WHERE media_id = ? 
            ORDER BY timestamp DESC
        ''', (media_id,))
        events = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return events
    
    @staticmethod
    def get_by_session(session_id):
        """Récupère tous les événements pour une session"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM visibility_event 
            WHERE session_id = ? 
            ORDER BY timestamp DESC
        ''', (session_id,))
        events = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return events


class UserSession:
    """Modèle pour les sessions utilisateur"""
    
    @staticmethod
    def create(page_url, user_agent, ip_address=None):
        """Crée une nouvelle session utilisateur"""
        session_id = str(uuid.uuid4())
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO user_session (session_id, page_url, user_agent, ip_address)
                VALUES (?, ?, ?, ?)
            ''', (session_id, page_url, user_agent, ip_address))
            conn.commit()
            return session_id
        except Exception as e:
            print(f"Erreur lors de la création de la session: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def end_session(session_id):
        """Termine une session utilisateur"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE user_session 
                SET end_time = CURRENT_TIMESTAMP 
                WHERE session_id = ?
            ''', (session_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la fermeture de la session: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def get_all():
        """Récupère toutes les sessions"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM user_session 
            ORDER BY start_time DESC
        ''')
        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return sessions
    
    @staticmethod
    def get_by_id(session_id):
        """Récupère une session spécifique"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM user_session 
            WHERE session_id = ?
        ''', (session_id,))
        session = cursor.fetchone()
        conn.close()
        return dict(session) if session else None


class MediaStats:
    """Modèle pour les statistiques agrégées des médias"""
    
    @staticmethod
    def update_stats(media_id):
        """Calcule et met à jour les statistiques pour un média"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Calcul des statistiques
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT session_id) as unique_viewers,
                COUNT(*) as total_events,
                AVG(visibility_percentage) as avg_visibility,
                SUM(duration_ms) as total_view_time
            FROM visibility_event
            WHERE media_id = ?
        ''', (media_id,))
        
        stats = cursor.fetchone()
        
        try:
            cursor.execute('''
                INSERT INTO media_stats 
                (media_id, total_views, total_impressions, average_visibility_percentage, total_view_time_ms, unique_viewers)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(media_id) DO UPDATE SET
                    total_views = ?,
                    total_impressions = ?,
                    average_visibility_percentage = ?,
                    total_view_time_ms = ?,
                    unique_viewers = ?,
                    last_updated = CURRENT_TIMESTAMP
            ''', (
                media_id,
                stats[1] or 0, stats[1] or 0, stats[2] or 0, stats[3] or 0, stats[0] or 0,  # INSERT
                stats[1] or 0, stats[1] or 0, stats[2] or 0, stats[3] or 0, stats[0] or 0   # UPDATE
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour des stats: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def get_stats(media_id):
        """Récupère les statistiques pour un média"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM media_stats WHERE media_id = ?', (media_id,))
        stats = dict(cursor.fetchone()) if cursor.fetchone() else None
        conn.close()
        return stats
    
    @staticmethod
    def get_all_stats():
        """Récupère les statistiques de tous les médias avec leurs infos (url, title)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                ms.*,
                m.url,
                m.title,
                m.type
            FROM media_stats ms
            LEFT JOIN media m ON ms.media_id = m.media_id
            ORDER BY ms.total_view_time_ms DESC
        ''')
        stats = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return stats
