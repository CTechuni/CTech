// Utilidades para manejo de autenticación
import { API_CONFIG, buildApiUrl } from '../config/api.js';

export class AuthManager {
    constructor() {
        this.tokenKey = 'authToken';
        this.userKey = 'user';
    }

    // Verificar si el usuario está autenticado
    isAuthenticated() {
        const token = this.getToken();
        return !!token && !this.isTokenExpired(token);
    }

    // Obtener token del localStorage
    getToken() {
        return localStorage.getItem(this.tokenKey);
    }

    // Obtener datos del usuario
    getUser() {
        const userStr = localStorage.getItem(this.userKey);
        return userStr ? JSON.parse(userStr) : null;
    }

    // Guardar datos de autenticación
    setAuthData(token, user) {
        localStorage.setItem(this.tokenKey, token);
        localStorage.setItem(this.userKey, JSON.stringify(user));
    }

    // Limpiar datos de autenticación
    clearAuthData() {
        localStorage.removeItem(this.tokenKey);
        localStorage.removeItem(this.userKey);
    }

    // Verificar si el token ha expirado
    isTokenExpired(token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const currentTime = Date.now() / 1000;
            return payload.exp < currentTime;
        } catch (error) {
            return true;
        }
    }

    // Login real al backend
    async login(email, password) {
        const url = buildApiUrl(API_CONFIG.AUTH.LOGIN);
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.detail || 'Credenciales inválidas');
        }

        const data = await response.json();
        this.setAuthData(data.access_token, data.user);
        return data;
    }

    // Logout
    logout() {
        this.clearAuthData();
    }

    // Helper para realizar peticiones autenticadas
    static async fetch(endpoint, options = {}) {
        const token = localStorage.getItem('authToken');
        const url = buildApiUrl(endpoint);
        
        const headers = {
            ...options.headers,
            'Authorization': token ? `Bearer ${token}` : '',
            'Content-Type': 'application/json'
        };

        const response = await fetch(url, { ...options, headers });
        
        if (response.status === 401) {
            localStorage.removeItem('authToken');
            window.location.href = '/login';
            return;
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || 'Error en la petición');
        }

        return response.json();
    }
}

export const authManager = new AuthManager();

export function requireAuth() {
    if (!authManager.isAuthenticated()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}
