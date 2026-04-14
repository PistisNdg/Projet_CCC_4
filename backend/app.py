from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_database
from models import Media, VisibilityEvent, UserSession, MediaStats
import os
from datetime import datetime

# Initialiser l'application Flask
app = Flask(__name__)
CORS(app)

# Initialiser la base de données au démarrage
init_database()

# ============================================================================
# ROUTES DE SESSION
# ============================================================================

@app.route('/api/session/create', methods=['POST'])
def create_session():
    """Crée une nouvelle session utilisateur"""
    try:
        data = request.get_json() or {}
        user_agent = request.headers.get('User-Agent', '')
        page_url = data.get('page_url', '/')
        
        session_id = UserSession.create(
            page_url=page_url,
            user_agent=user_agent,
            ip_address=request.remote_addr
        )
        
        if session_id:
            return jsonify({
                'success': True,
                'session_id': session_id,
                'message': 'Session créée avec succès'
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de la création de la session'
            }), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/session/end/<session_id>', methods=['POST'])
def end_session(session_id):
    """Termine une session utilisateur"""
    try:
        if UserSession.end_session(session_id):
            return jsonify({
                'success': True,
                'message': 'Session terminée avec succès'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de la fermeture de la session'
            }), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/sessions', methods=['GET'])
def get_all_sessions():
    """Récupère toutes les sessions enregistrées"""
    try:
        sessions = UserSession.get_all()
        return jsonify({
            'success': True,
            'sessions': sessions,
            'total_sessions': len(sessions)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/session/<session_id>', methods=['GET'])
def get_session_details(session_id):
    """Récupère les détails d'une session"""
    try:
        session = UserSession.get_by_id(session_id)
        if session:
            events = VisibilityEvent.get_by_session(session_id)
            return jsonify({
                'success': True,
                'session': session,
                'events_count': len(events),
                'events': events
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Session non trouvée'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================================================
# ROUTES DE TRACKING DE VISIBILITÉ
# ============================================================================

@app.route('/api/tracking/record', methods=['POST'])
def record_visibility():
    """Enregistre un événement de visibilité média"""
    try:
        data = request.get_json()
        
        if not data or 'media_id' not in data or 'session_id' not in data:
            return jsonify({
                'success': False,
                'message': 'Données manquantes: media_id et session_id requis'
            }), 400
        
        # Enregistrer l'événement
        if VisibilityEvent.record(
            media_id=data['media_id'],
            session_id=data['session_id'],
            event_data=data
        ):
            # Mettre à jour les statistiques
            MediaStats.update_stats(data['media_id'])
            
            return jsonify({
                'success': True,
                'message': 'Événement enregistré avec succès'
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de l\'enregistrement'
            }), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/tracking/batch', methods=['POST'])
def batch_record_visibility():
    """Enregistre plusieurs événements de visibilité en batch"""
    try:
        data = request.get_json()
        
        if not data or 'events' not in data:
            return jsonify({
                'success': False,
                'message': 'Format invalide: "events" est requis'
            }), 400
        
        events = data['events']
        success_count = 0
        
        for event in events:
            if 'media_id' in event and 'session_id' in event:
                if VisibilityEvent.record(
                    media_id=event['media_id'],
                    session_id=event['session_id'],
                    event_data=event
                ):
                    success_count += 1
                    MediaStats.update_stats(event['media_id'])
        
        return jsonify({
            'success': True,
            'processed': success_count,
            'total': len(events),
            'message': f'{success_count}/{len(events)} événements enregistrés'
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================================================
# ROUTES DE GESTION DES MÉDIAS
# ============================================================================

@app.route('/api/media', methods=['GET'])
def get_all_media():
    """Récupère tous les médias"""
    try:
        media = Media.get_all()
        return jsonify({
            'success': True,
            'media': media
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/media/create', methods=['POST'])
def create_media():
    """Crée une nouvelle entrée média"""
    try:
        data = request.get_json()
        
        required_fields = ['media_id', 'title', 'type', 'url']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': f'Champs requis: {", ".join(required_fields)}'
            }), 400
        
        if Media.create(
            media_id=data['media_id'],
            title=data['title'],
            media_type=data['type'],
            url=data['url']
        ):
            # Initialiser les statistiques
            MediaStats.update_stats(data['media_id'])
            
            return jsonify({
                'success': True,
                'message': 'Média créé avec succès'
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de la création du média'
            }), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================================================
# ROUTES DE STATS ET ANALYTICS
# ============================================================================

@app.route('/api/stats/media/<media_id>', methods=['GET'])
def get_media_stats(media_id):
    """Récupère les statistiques pour un média spécifique"""
    try:
        stats = MediaStats.get_stats(media_id)
        
        if stats:
            # Récupérer aussi les événements de visibilité
            events = VisibilityEvent.get_by_media(media_id)
            
            return jsonify({
                'success': True,
                'stats': stats,
                'events_count': len(events)
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Aucune statistique trouvée pour ce média'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/stats/all', methods=['GET'])
def get_all_stats():
    """Récupère les statistiques de tous les médias"""
    try:
        all_stats = MediaStats.get_all_stats()
        
        return jsonify({
            'success': True,
            'stats': all_stats,
            'total_media': len(all_stats)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/stats/media/<media_id>/timeline', methods=['GET'])
def get_visibility_timeline(media_id):
    """Récupère la timeline de visibilité pour un média"""
    try:
        events = VisibilityEvent.get_by_media(media_id)
        
        # Grouper par heure
        timeline = {}
        for event in events:
            timestamp = event['timestamp'][:13]  # YYYY-MM-DD HH
            if timestamp not in timeline:
                timeline[timestamp] = {
                    'count': 0,
                    'avg_visibility': 0,
                    'total_duration': 0
                }
            timeline[timestamp]['count'] += 1
            timeline[timestamp]['total_duration'] += event['duration_ms'] or 0
        
        # Calculer les moyennes
        for hour in timeline:
            count = timeline[hour]['count']
            if count > 0:
                timeline[hour]['avg_visibility'] = timeline[hour]['total_duration'] / count
        
        return jsonify({
            'success': True,
            'media_id': media_id,
            'timeline': timeline
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de santé de l'API"""
    return jsonify({
        'success': True,
        'status': 'API Media Tracking est opérationnelle',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/', methods=['GET'])
def index():
    """Page d'accueil"""
    return jsonify({
        'name': 'Media Visibility Tracking System',
        'version': '1.0.0',
        'description': 'API pour le suivi de visibilité des médias',
        'endpoints': {
            'session': '/api/session/create, /api/session/end/<id>',
            'tracking': '/api/tracking/record, /api/tracking/batch',
            'media': '/api/media, /api/media/create',
            'stats': '/api/stats/all, /api/stats/media/<id>, /api/stats/media/<id>/timeline',
            'health': '/api/health'
        }
    }), 200


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Route non trouvée'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Erreur serveur interne'
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
