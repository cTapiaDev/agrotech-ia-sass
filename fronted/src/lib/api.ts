import axios from "axios";
import { env } from '$env/dynamic/public';
import { toaster } from "./toast.svelte";

const api = axios.create({
    baseURL: env.PUBLIC_API_URL,
    headers: { 'Content-Type': 'application/json' }
})

// Interceptamos la petición: Agrega el JWT en caso de existir.
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) config.headers.Authorization = `Bearer ${token}`
        return config;
    },
    (error) => Promise.reject(error)
);

// Interceptamos la petición: Lógica asíncrona para refrescar el token (Refresh Token)
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response) {
            const status = error.response.status;

            if (status === 401 && !originalRequest.__retry) {
                originalRequest._retry = true;

                try {
                    const refreshToken = localStorage.getItem('refresh_token');

                    const refreshResponse = await axios.post(`${env.PUBLIC_API_URL}/token/refresh/`, {
                        refresh: refreshToken
                    });

                    const newAccessToken = refreshResponse.data.access;
                    localStorage.setItem('access_token', newAccessToken);
                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`

                    return api(originalRequest);
                } catch (refreshError) {
                    // localStorage.removeItem('access_token');
                    // localStorage.removeItem('refresh_token');
                    localStorage.clear();
                    window.location.href = '/login';
                    return Promise.reject(refreshError);
                }

                if (status === 400) {
                    const data = error.response.data;
                    const errorMessages = Object.values(data).flat().join(' | ');
                    toaster.add(`Validación fallida: ${errorMessages}`, 'warning');
                }

                if (status >= 500) {
                    toaster.add('Error crítico en el servidor', 'error')
                }
            } else {
                toaster.add('No se puede conectar con la API', 'error')
            }
        }
        return Promise.reject(error);
    }
)

export default api;