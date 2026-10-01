import api from '$lib/api';
import { redirect } from '@sveltejs/kit'
import type { PageLoad } from './$types';

export const ssr = false;

export const load: PageLoad = async () => {
    try {
        const response = await api.get('/crops/');

        return {
            crops: response.data
        };

    } catch (error) {
        throw redirect(307, '/login');
    }
}