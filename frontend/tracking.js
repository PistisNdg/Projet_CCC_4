/**
 * Module de Tracking de Visibilité Média
 * Détecte la visibilité des éléments dans le viewport et envoie les données à l'API
 */

class MediaVisibilityTracker {
    constructor(apiBaseUrl = 'http://localhost:5000/api') {
        this.apiBaseUrl = apiBaseUrl;
        this.sessionId = null;
        this.trackedMedia = new Map(); // media_id -> {element, data, startTime}
        this.eventBatch = [];
        this.batchSize = 10;
        this.batchTimeout = 5000; // 5 secondes
        this.batchTimer = null;
        this.isOnline = navigator.onLine;
        this.periodicReportInterval = 3000; // Rapporter la visibilité toutes les 3 secondes
        this.periodicReportTimer = null;
        this.isReady = false; // Flag pour indiquer que l'init est terminée
        
        this.init();
    }
    
    /**
     * Initialise le tracker
     */
    async init() {
        console.log('🎬 Initialisation du Media Visibility Tracker');
        
        // Créer une session et attendre vraiment
        let sessionCreated = false;
        let attempts = 0;
        while (!sessionCreated && attempts < 5) {
            await this.createSession();
            if (this.sessionId) {
                sessionCreated = true;
            } else {
                attempts++;
                console.warn(`⚠️ Tentative ${attempts} de création de session...`);
                await new Promise(resolve => setTimeout(resolve, 500));
            }
        }
        
        if (!sessionCreated) {
            console.error('❌ Impossible de créer une session après 5 tentatives');
        }
        
        // Observer les changements de visibilité
        this.setupIntersectionObserver();
        
        // Gérer la visibilité de la page
        this.setupPageVisibilityHandler();
        
        // Gérer l'état du réseau
        this.setupNetworkHandlers();
        
        // Démarrer le rapport périodique SEULEMENT quand la session est prête
        if (this.sessionId) {
            this.startPeriodicReporting();
        }
        
        // Marquer comme prêt
        this.isReady = true;
        console.log('✓ Tracker prêt');
        
        // Terminer la session à la fermeture
        window.addEventListener('beforeunload', () => {
            this.stopPeriodicReporting();
            this.endSession();
            this.flushBatch(); // Envoyer les derniers événements
        });
    }
    
    /**
     * Crée une nouvelle session utilisateur
     */
    async createSession() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/session/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    page_url: window.location.href
                })
            });
            
            const data = await response.json();
            if (data.success) {
                this.sessionId = data.session_id;
                console.log(`✓ Session créée: ${this.sessionId}`);
                localStorage.setItem('mediaTrackerSessionId', this.sessionId);
            } else {
                console.error('❌ Erreur lors de la création de session:', data.message);
            }
        } catch (error) {
            console.error('❌ Erreur réseau lors de la création de session:', error);
        }
    }
    
    /**
     * Termine la session
     */
    async endSession() {
        if (!this.sessionId) return;
        
        try {
            await fetch(`${this.apiBaseUrl}/session/end/${this.sessionId}`, {
                method: 'POST',
                keepalive: true // Important pour les requêtes avant décharge
            });
            console.log('✓ Session terminée');
        } catch (error) {
            console.error('❌ Erreur lors de la fermeture de la session:', error);
        }
    }
    
    /**
     * Configure l'Intersection Observer pour tracker la visibilité
     */
    setupIntersectionObserver() {
        const options = {
            root: null,
            rootMargin: '0px',
            threshold: [0, 0.25, 0.5, 0.75, 1.0] // Déclencher à différents niveaux
        };
        
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                this.handleVisibilityChange(entry);
            });
        }, options);
        
        console.log('✓ Intersection Observer configuré');
    }
    
    /**
     * Enregistre un élément média pour tracking
     * @param {HTMLElement} element - L'élément à tracker
     * @param {string} mediaId - ID unique du média
     * @param {string} mediaType - Type du média (image, video, text)
     * @param {Object} metadata - Métadonnées additionnelles
     */
    trackElement(element, mediaId, mediaType = 'unknown', metadata = {}) {
        if (!element || !mediaId) {
            console.warn('⚠️ Element ou mediaId manquant');
            return;
        }
        
        // Attendre que le tracker soit prêt
        if (!this.isReady) {
            console.warn('⚠️ Tracker non initialisé, retry dans 100ms');
            setTimeout(() => this.trackElement(element, mediaId, mediaType, metadata), 100);
            return;
        }
        
        // Ajouter des attributs de data pour identification
        element.setAttribute('data-media-id', mediaId);
        element.setAttribute('data-media-type', mediaType);
        
        // Stocker les données de tracking
        this.trackedMedia.set(mediaId, {
            element: element,
            mediaId: mediaId,
            mediaType: mediaType,
            isVisible: false,
            startTime: null,
            visibilityPercentage: 0,
            metadata: metadata,
            lastUpdate: Date.now()
        });
        
        // Observer cet élément
        this.observer.observe(element);
        console.log(`✓ Tracking configuré pour: ${mediaId} (${mediaType})`);
    }
    
    /**
     * Gère les changements de visibilité
     */
    handleVisibilityChange(entry) {
        const mediaId = entry.target.getAttribute('data-media-id');
        if (!mediaId || !this.trackedMedia.has(mediaId)) return;
        
        const tracker = this.trackedMedia.get(mediaId);
        const isNowVisible = entry.isIntersecting;
        
        // Calculer le pourcentage de visibilité
        let visibilityPercentage = 0;
        if (entry.intersectionRatio > 0) {
            visibilityPercentage = Math.round(entry.intersectionRatio * 100);
        }
        
        // Si passage de invisible à visible
        if (isNowVisible && !tracker.isVisible) {
            tracker.isVisible = true;
            tracker.startTime = Date.now();
            console.log(`👁️ Média visible: ${mediaId} (${visibilityPercentage}%)`);
        }
        // Si passage de visible à invisible
        else if (!isNowVisible && tracker.isVisible) {
            tracker.isVisible = false;
            const duration = Date.now() - tracker.startTime;
            
            // Enregistrer l'événement
            this.recordEvent({
                media_id: mediaId,
                event_type: 'view_complete',
                visibility_percentage: tracker.visibilityPercentage,
                duration_ms: duration,
                device_type: this.getDeviceType(),
                viewport_width: window.innerWidth,
                viewport_height: window.innerHeight
            });
            
            console.log(`👁️ Média hors écran: ${mediaId} (durée: ${duration}ms)`);
        }
        
        // Mettre à jour le pourcentage de visibilité
        if (isNowVisible) {
            tracker.visibilityPercentage = visibilityPercentage;
            tracker.lastUpdate = Date.now();
        }
    }
    
    /**
     * Enregistre un événement de tracking
     */
    recordEvent(eventData, retryCount = 0) {
        if (!this.sessionId) {
            // Retry jusqu'à 3 fois avec délai exponentiel
            if (retryCount < 3) {
                const delay = 100 * Math.pow(2, retryCount); // 100ms, 200ms, 400ms
                console.warn(`⚠️ Session non initialisée - Retry ${retryCount + 1}/3 dans ${delay}ms`);
                setTimeout(() => this.recordEvent(eventData, retryCount + 1), delay);
                return;
            } else {
                console.error('❌ Session impossible à initialiser après 3 tentatives');
                return;
            }
        }
        
        // Ajouter l'ID de session
        eventData.session_id = this.sessionId;
        
        // Ajouter au batch
        this.eventBatch.push(eventData);
        console.log(`📊 Événement ajouté au batch (${this.eventBatch.length}/${this.batchSize})`);
        
        // Envoyer si le batch est plein
        if (this.eventBatch.length >= this.batchSize) {
            this.flushBatch();
        } else if (!this.batchTimer) {
            // Démarrer le timer si pas déjà actif
            this.batchTimer = setTimeout(() => this.flushBatch(), this.batchTimeout);
        }
    }
    
    /**
     * Envoie le batch d'événements à l'API
     */
    async flushBatch() {
        if (this.eventBatch.length === 0) return;
        
        clearTimeout(this.batchTimer);
        this.batchTimer = null;
        
        const eventsToSend = [...this.eventBatch];
        this.eventBatch = [];
        
        try {
            console.log(`📤 Envoi de ${eventsToSend.length} événement(s) à l'API...`);
            
            const response = await fetch(`${this.apiBaseUrl}/tracking/batch`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    events: eventsToSend
                })
            });
            
            const data = await response.json();
            if (data.success) {
                console.log(`✓ ${data.processed} événement(s) enregistré(s) avec succès`);
            } else {
                console.error('❌ Erreur:', data.message);
                // Remettre les événements en queue en cas d'erreur
                this.eventBatch.unshift(...eventsToSend);
            }
        } catch (error) {
            console.error('❌ Erreur réseau lors de l\'envoi:', error);
            // Remettre les événements en queue
            this.eventBatch.unshift(...eventsToSend);
        }
    }
    
    /**
     * Détecte le type d'appareil
     */
    getDeviceType() {
        const ua = navigator.userAgent.toLowerCase();
        if (/mobile|android|iphone|ipod|blackberry|iemobile|opera mini/.test(ua)) {
            return 'mobile';
        } else if (/tablet|ipad/.test(ua)) {
            return 'tablet';
        }
        return 'desktop';
    }
    
    /**
     * Gère les changements de visibilité de page
     */
    setupPageVisibilityHandler() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                console.log('📵 Page cachée - Flush du batch');
                this.flushBatch();
            } else {
                console.log('📱 Page visible');
            }
        });
    }
    
    /**
     * Gère l'état du réseau
     */
    setupNetworkHandlers() {
        window.addEventListener('online', () => {
            console.log('🌐 Connexion rétablie - Flush du batch');
            this.isOnline = true;
            if (this.eventBatch.length > 0) {
                this.flushBatch();
            }
        });
        
        window.addEventListener('offline', () => {
            console.log('📴 Connexion perdue - Batch en attente');
            this.isOnline = false;
        });
    }

    /**
     * Démarre le rapport périodique de visibilité
     */
    startPeriodicReporting() {
        this.periodicReportTimer = setInterval(() => {
            // Rapporter chaque média actuellement visible
            this.trackedMedia.forEach((tracker, mediaId) => {
                if (tracker.isVisible && tracker.startTime) {
                    const currentDuration = Date.now() - tracker.startTime;
                    this.recordEvent({
                        media_id: mediaId,
                        event_type: 'periodic_view',
                        visibility_percentage: tracker.visibilityPercentage,
                        duration_ms: currentDuration,
                        device_type: this.getDeviceType(),
                        viewport_width: window.innerWidth,
                        viewport_height: window.innerHeight
                    });
                }
            });
        }, this.periodicReportInterval);
    }

    /**
     * Arrête le rapport périodique
     */
    stopPeriodicReporting() {
        if (this.periodicReportTimer) {
            clearInterval(this.periodicReportTimer);
            this.periodicReportTimer = null;
        }
    }

    /**
     * Obtient les stats du tracker
     */
    getStats() {
        return {
            sessionId: this.sessionId,
            trackedMediaCount: this.trackedMedia.size,
            pendingEvents: this.eventBatch.length,
            trackedMedia: Array.from(this.trackedMedia.values()).map(t => ({
                mediaId: t.mediaId,
                type: t.mediaType,
                isVisible: t.isVisible,
                visibilityPercentage: t.visibilityPercentage
            }))
        };
    }
}

// Exposition globale pour utilisation dans le HTML
window.MediaVisibilityTracker = MediaVisibilityTracker;
