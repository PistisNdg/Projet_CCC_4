/**
 * Module API pour communiquer avec le serveur Flask
 */

class MediaAPI {
    constructor(baseUrl = 'http://localhost:5000/api') {
        this.baseUrl = baseUrl;
    }

    /**
     * Crée un nouveau média dans la base de données
     */
    async createMedia(mediaId, title, mediaType, url) {
        try {
            const response = await fetch(`${this.baseUrl}/media/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    media_id: mediaId,
                    title: title,
                    type: mediaType,
                    url: url
                })
            });
            const data = await response.json();
            return data.success;
        } catch (error) {
            console.error('❌ Erreur lors de la création du média:', error);
            return false;
        }
    }

    /**
     * Récupère tous les médias
     */
    async getAllMedia() {
        try {
            const response = await fetch(`${this.baseUrl}/media`);
            const data = await response.json();
            return data.success ? data.media : [];
        } catch (error) {
            console.error('❌ Erreur lors de la récupération des médias:', error);
            return [];
        }
    }

    /**
     * Récupère les stats pour un média spécifique
     */
    async getMediaStats(mediaId) {
        try {
            const response = await fetch(`${this.baseUrl}/stats/media/${mediaId}`);
            const data = await response.json();
            return data.success ? data.stats : null;
        } catch (error) {
            console.error('❌ Erreur lors de la récupération des stats:', error);
            return null;
        }
    }

    /**
     * Récupère les stats de tous les médias
     */
    async getAllStats() {
        try {
            const response = await fetch(`${this.baseUrl}/stats/all`);
            const data = await response.json();
            return data.success ? data.stats : [];
        } catch (error) {
            console.error('❌ Erreur lors de la récupération des stats:', error);
            return [];
        }
    }

    /**
     * Récupère la timeline de visibilité d'un média
     */
    async getVisibilityTimeline(mediaId) {
        try {
            const response = await fetch(`${this.baseUrl}/stats/media/${mediaId}/timeline`);
            const data = await response.json();
            return data.success ? data.timeline : {};
        } catch (error) {
            console.error('❌ Erreur lors de la récupération timeline:', error);
            return {};
        }
    }
}

// Exposition globale
const api = new MediaAPI('http://localhost:5000/api');

/**
 * Fonction helper pour créer un média (utilisée dans test_page.html)
 */
async function createMedia(mediaId, title, mediaType, url) {
    return api.createMedia(mediaId, title, mediaType, url);
}
