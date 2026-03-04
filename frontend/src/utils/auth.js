// Utilidades para manejo de autenticación
import { API_CONFIG, buildApiUrl } from '../config/api.js';

export class AuthManager {
    constructor() {
        this.tokenKey = 'authToken';
        this.userKey = 'user';
        this.lastTokenKey = 'lastAuthToken'; // Para detectar cambios entre pestañas
        this.authChangeListeners = [];
        this.setupStorageListener();
    }

    // ── Setup: Sincronización entre pestañas ──────────────────────────────────

    /**
     * Detecta cambios de storage (logout/login en otra pestaña)
     */
    setupStorageListener() {
        if (typeof window === 'undefined') return;

        window.addEventListener('storage', (event) => {
            if (event.key === this.tokenKey) {
                // El token fue modificado en otra pestaña
                if (!event.newValue) {
                    // Token fue eliminado (logout en otra pestaña)
                    this.handleRemoteLogout();
                } else if (event.newValue !== localStorage.getItem(this.tokenKey)) {
                    // Token cambió (login con otra cuenta en otra pestaña)
                    this.handleRemoteLogin();
                }
            }
        });

        // Beofre unload: Notificar otras pestañas si es logout intencional
        window.addEventListener('beforeunload', () => {
            if (!this.isAuthenticated()) {
                // Ya está deslogueado, no hay nada que sincronizar
            }
        });
    }

    handleRemoteLogout() {
        // Otra pestaña hizo logout
        this.clearAuthData(false); // false = no propagar (ya lo hizo otra pestaña)
        this.notifyAuthChange('logout');
        // No redirigir aquí, dejar que el componente lo maneje
    }

    handleRemoteLogin() {
        // Otra pestaña hizo login (posiblemente con otro usuario/rol)
        const newToken = localStorage.getItem(this.tokenKey);
        const newUser = localStorage.getItem(this.userKey);
        this.notifyAuthChange('login', newToken ? JSON.parse(newUser) : null);
    }

    // ── Event listeners ────────────────────────────────────────────────────────

    /**
     * Escucha cambios de autenticación
     */
    onAuthChange(callback) {
        this.authChangeListeners.push(callback);
    }

    notifyAuthChange(action, user = null) {
        this.authChangeListeners.forEach(cb => {
            try { cb({ action, user }); }
            catch (e) { /* silently fail */ }
        });
    }

    // ── Estado ────────────────────────────────────────────────────────────────

    isAuthenticated() {
        const token = this.getToken();
        return !!token && !this.isTokenExpired(token);
    }

    getToken() {
        return localStorage.getItem(this.tokenKey);
    }

    getUser() {
        const raw = localStorage.getItem(this.userKey);
        try { return raw ? JSON.parse(raw) : null; }
        catch { return null; }
    }

    getRole() {
        return (this.getUser()?.role || '').toLowerCase();
    }

    // ── Persistencia ──────────────────────────────────────────────────────────

    setAuthData(token, user) {
        localStorage.setItem(this.tokenKey, token);
        localStorage.setItem(this.userKey, JSON.stringify(user));
        localStorage.setItem(this.lastTokenKey, token);
        this.notifyAuthChange('login', user);
    }

    clearAuthData(propagate = true) {
        localStorage.removeItem(this.tokenKey);
        localStorage.removeItem(this.userKey);
        localStorage.removeItem(this.lastTokenKey);
        if (propagate) {
            this.notifyAuthChange('logout');
        }
    }

    // ── Token ─────────────────────────────────────────────────────────────────

    isTokenExpired(token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            return payload.exp ? payload.exp < Date.now() / 1000 : false;
        } catch {
            return true;
        }
    }

    // ── Auth actions ──────────────────────────────────────────────────────────

    async login(email, password) {
        const url = buildApiUrl(API_CONFIG.AUTH.LOGIN);

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const err = await response.json().catch(() => ({}));

                // Handle Pydantic array detail or string
                const detail = Array.isArray(err.detail)
                    ? err.detail.map(e => e.msg).join(', ')
                    : (err.detail || 'Credenciales inválidas');

                throw new Error(detail);
            }

            const data = await response.json();
            console.debug('authManager.login received', data);
            this.setAuthData(data.access_token, data.user);
            console.debug('authManager.login stored token, user', data.user);
            return data;
        } catch (error) {
            console.error('authManager.login error', error);
            throw error;
        }
    }

    async register(userData) {
        // Mapear los nombres de campo del formulario a los que espera el backend
        const payload = {
            email: userData.email,
            password: userData.password,
            name_user: userData.fullName || userData.name_user,
            community_id: userData.community_id || userData.community || null,
            invite_code: userData.inviteCode || userData.invite_code || null,
            rol_id: userData.rol_id || null
        };

        // El backend ignora campos null/undefined
        return AuthManager.fetch('/users/register', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
    }

    logout() {
        this.clearAuthData();
        window.location.href = '/';
    }

    // ── Peticiones autenticadas (estático) ────────────────────────────────────

    /**
     * Realiza una petición autenticada al backend.
     * @param {string} endpoint  - Ruta relativa, ej: '/users/'
     * @param {RequestInit} options
     */
    static async fetch(endpoint, options = {}) {
        const token = localStorage.getItem('authToken');
        const url = buildApiUrl(endpoint);

        // Si el body es FormData, el navegador debe establecer el Content-Type con el boundary correcto.
        const headers = { ...options.headers };

        if (!(options.body instanceof FormData)) {
            headers['Content-Type'] = headers['Content-Type'] || 'application/json';
        }

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(url, { ...options, headers });

        if (response.status === 401) {
            // Token inválido, expirado o revocado
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
            localStorage.removeItem('lastAuthToken');
            window.location.href = '/';
            return;
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || `Error ${response.status}`);
        }

        // Respuestas 204 No Content no tienen body
        const contentType = response.headers.get('content-type') || '';
        if (response.status === 204 || !contentType.includes('application/json')) return null;

        return response.json();
    }
}

// ── Instancia global y helpers ────────────────────────────────────────────────

export const authManager = new AuthManager();

/** Redirige al inicio si el usuario no está autenticado. */
export function requireAuth() {
    /**
     * IMPLEMENTACIÓN ORIGINAL (COMENTADA TEMPORALMENTE)
     *
     * if (!authManager.isAuthenticated()) {
     *     window.location.href = '/';
     *     return false;
     * }
     * return true;
     */

    // Autenticación deshabilitada para permitir navegar sin login
    return true;
}

/** Redirige al inicio si el usuario no tiene el rol esperado. */
export function requireRole(role) {
    /**
     * IMPLEMENTACIÓN ORIGINAL (COMENTADA TEMPORALMENTE)
     *
     * if (!requireAuth()) return false;
     * const userRole = authManager.getRole();
     * console.debug('requireRole check', role, 'currentRole', userRole);
     * if (!userRole.includes(role.toLowerCase())) {
     *     console.warn('requireRole failed, redirecting to /', userRole, role);
     *     window.location.href = '/';
     *     return false;
     * }
     * return true;
     */

    // Comprobación de rol deshabilitada para desarrollo
    return true;
}

/**
 * Event listener para cambios de autenticación
 * Útil para sincronizar UI entre pestañas
 */
export function onAuthStateChanged(callback) {
    authManager.onAuthChange(callback);
}
