// api.js
import { keycloak } from "./auth.js";

/**
 * Hilfsfunktion: lokale ISO ohne Zeitzone (YYYY-MM-DDTHH:mm:ss)
 */
function msToLocalIso(ms) {
    const d = new Date(Number(ms));
    if (isNaN(d.getTime())) return null;
    const pad = (n) => String(n).padStart(2, "0");
    const date = `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
    const time = `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
    return `${date}T${time}`;
}

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
        // Versuche, die Response als Text/JSON zu lesen für bessere Fehlermeldung
        let bodyText = null;
        try {
            bodyText = await response.text();
        } catch (e) {
            bodyText = "<could not read response body>";
        }
        console.error("[api] response not ok", response.status, bodyText);
        const err = new Error(`API error: ${response.status}`);
        err.status = response.status;
        err.body = bodyText;
        throw err;
    }

    const json = await response.json();
    console.debug("[api] response json preview", json && json.labels ? { labels0: json.labels[0], labelsLen: json.labels.length } : json);
    return json;
}

/**
 * getSensorRange(params)
 * - bevorzugt: { fromMs, toMs } (epoch ms)
 * - fallback: { from, to } (local ISO ohne Z)
 *
 * Wenn ein Request mit fromMs/toMs mit 400 beantwortet wird, versucht diese Funktion
 * automatisch einen zweiten Request mit from/to (lokale ISO) und loggt die Serverantworten.
 */
export async function getSensorRange(params) {
    if (!params) throw new Error("getSensorRange: missing params");

    // Helper: baut Querystring aus Objekt
    const buildQuery = (p) => {
        const qp = new URLSearchParams();
        if (p.fromMs != null) qp.append("fromMs", String(p.fromMs));
        if (p.toMs != null) qp.append("toMs", String(p.toMs));
        if (p.from != null) qp.append("from", p.from);
        if (p.to != null) qp.append("to", p.to);
        return qp.toString();
    };

    // 1) Wenn fromMs vorhanden -> erster Versuch mit epoch ms
    if (params.fromMs != null || params.toMs != null) {
        const q = buildQuery({ fromMs: params.fromMs, toMs: params.toMs });
        console.debug("[api] trying with fromMs/toMs", { fromMs: params.fromMs, toMs: params.toMs });
        try {
            return await apiGet(`/sensordata/range?${q}`);
        } catch (err) {
            // Wenn 400/422 (Bad Request / Unprocessable) -> Fallback auf ISO strings
            if (err && (err.status === 400 || err.status === 422)) {
                console.warn("[api] server rejected fromMs/toMs, trying fallback with local ISO strings. server message:", err.body);
                // Baue lokale ISO strings aus ms
                const fallback = {};
                if (params.fromMs != null) fallback.from = msToLocalIso(params.fromMs);
                if (params.toMs != null) fallback.to = msToLocalIso(params.toMs);
                console.debug("[api] fallback params", fallback);
                const q2 = buildQuery(fallback);
                try {
                    return await apiGet(`/sensordata/range?${q2}`);
                } catch (err2) {
                    console.error("[api] fallback also failed", err2.status, err2.body);
                    throw err2;
                }
            }
            // andere Fehler weiterwerfen
            throw err;
        }
    }

    // 2) Wenn keine ms, dann normal mit from/to
    const q = buildQuery(params);
    console.debug("[api] using from/to", params);
    return apiGet(`/sensordata/range?${q}`);
}
