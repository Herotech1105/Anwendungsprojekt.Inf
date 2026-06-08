// api.js
import { keycloak } from "./auth.js";

async function apiGet(path) {
    const url = `https://local.kleber.data/api${path}`;
    console.debug("[api] GET", url);

    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + keycloak.token
        }
    });

    if (!response.ok) {
        console.error("[api] response not ok", response.status);
        throw new Error(`API error: ${response.status}`);
    }

    const json = await response.json();
    console.debug("[api] response json preview", json && json.labels ? { labels0: json.labels[0], labelsLen: json.labels.length } : json);
    return json;
}

/**
 * Unterstützt params: { fromMs, toMs } bevorzugt; fallback { from, to }.
 */
export async function getSensorRange(params) {
    if (!params) throw new Error("getSensorRange: missing params");
    const qp = new URLSearchParams();

    if (params.fromMs != null) {
        qp.append("fromMs", String(params.fromMs));
        console.debug("[api] using fromMs", params.fromMs);
    } else if (params.from != null) {
        qp.append("from", params.from);
        console.debug("[api] using from (iso local)", params.from);
    }

    if (params.toMs != null) {
        qp.append("toMs", String(params.toMs));
        console.debug("[api] using toMs", params.toMs);
    } else if (params.to != null) {
        qp.append("to", params.to);
        console.debug("[api] using to (iso local)", params.to);
    }

    return apiGet(`/sensordata/range?${qp.toString()}`);
}
