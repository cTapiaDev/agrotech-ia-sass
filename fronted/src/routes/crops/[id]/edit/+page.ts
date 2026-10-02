import api from "$lib/api";
import { redirect } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = async ({ params }) => {
    try {
        const response = await api.get(`/crops/${params.id}/`);
        return {
            crop: response.data
        };
    } catch (error) {
        throw redirect(307, '/')
    }
}