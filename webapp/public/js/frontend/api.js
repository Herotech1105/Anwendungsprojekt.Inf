// js/frontend/api.js
import { keycloak } from "./auth.js";

async function apiGet(path) {
    const res = await fetch(`/api${path}`, {
        headers: {
            "Authorization": "Bearer " + keycloak.token
        }
    });

    if (!res.ok) throw new Error("API error: " + res.status);
    return res.json();
}

export function getSensorRange(from, to) {
    const q = new URLSearchParams({ from, to }).toString();
    return apiGet(`/sensordata/range?${q}`);
}

export async function exportDatabase() {
    const res = await fetch("/api/admin/export", {
        headers: { Authorization: `Bearer ${keycloak.token}` }
    });

    if (!res.ok) {
        alert("Export fehlgeschlagen: " + res.status);
        return;
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "myapp_export.sql";
    a.click();
    URL.revokeObjectURL(url);
}
