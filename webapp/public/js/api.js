import { keycloak } from "./auth.js";

async function apiGet(path) {
    const url = `https://local.kleber.data/api${path}`;

    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + keycloak.token
        }
    });

    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }

    return response.json();
}

export async function getSensorRange(from, to) {
    const query = `?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}`;
    return apiGet(`/sensordata/range${query}`);
}
