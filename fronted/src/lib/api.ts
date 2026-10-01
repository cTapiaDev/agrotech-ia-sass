import axios from "axios";
import { env } from '$env/dynamic/public';

const api = axios.create({
    baseURL: env.PUBLIC_API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
})

// Interceptamos la petición: Agrega el JWT en caso de existir.
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Interceptamos la petición: Lógica asíncrona para refrescar el token (Refresh Token)
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response.status === 401 && !originalRequest.__retry) {
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
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
)

export default api;