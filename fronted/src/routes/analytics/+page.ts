import api from "$lib/api";
import type { PageLoad } from "../$types";

export const ssr = false;

export const load: PageLoad = async () => {
    try {
        const response = await api.get('/weather_logs/');
        return {
            logs: response.data
        };
    } catch (error) {
        console.error('Fallo al obtener los registros de MongoDB:', error);
        return {
            logs: []
        }
    }
}