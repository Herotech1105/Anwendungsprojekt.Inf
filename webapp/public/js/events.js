// events.js
import { logout } from "./auth.js";

/**
 * Liefert lokale ISO ohne Zeitzone (YYYY-MM-DDTHH:mm:ss)
 */
function localInputToLocalIso(inputValue) {
    if (!inputValue) return null;
    const [datePart, timePartRaw] = inputValue.split("T");
    if (!datePart || !timePartRaw) return null;
    const timePart = timePartRaw.length === 5 ? `${timePartRaw}:00` : timePartRaw;
    return `${datePart}T${timePart}`;
}

/**
 * Konvertiert datetime-local in epoch ms (interpretiert als lokale Zeit)
 */
function localInputToMs(inputValue) {
    if (!inputValue) return null;
    const d = new Date(inputValue); // interpretiert als lokale Zeit
    if (isNaN(d.getTime())) return null;
    return d.getTime();
}

export function initEvents() {
    const loadBtn = document.getElementById("loadDataBtn");
    if (loadBtn) {
        loadBtn.addEventListener("click", () => {
            const fromLocal = document.getElementById("from").value;
            const toLocal = document.getElementById("to").value;

            if (!fromLocal) {
                alert("Bitte Startzeit auswählen");
                return;
            }

            // ms (bevorzugt)
            const fromMs = localInputToMs(fromLocal);
            // Wenn kein "to" gewählt wurde, setze toMs auf jetzt (sonst 400 vom Server)
            const toMs = toLocal ? localInputToMs(toLocal) : Date.now();

            // ISO local fallback (falls Backend Strings erwartet)
            const fromIsoLocal = localInputToLocalIso(fromLocal);
            const toIsoLocal = toLocal ? localInputToLocalIso(toLocal) : localInputToLocalIso(new Date().toISOString().slice(0,19));

            console.debug("[events] user selected", {
                fromLocal, toLocal, fromMs, toMs, fromIsoLocal, toIsoLocal
            });

            window.dispatchEvent(new CustomEvent("loadRange", {
                detail: { fromMs, toMs, fromIsoLocal, toIsoLocal }
            }));
        });
    } else {
        console.warn("[events] loadDataBtn not found");
    }

    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            logout();
        });
    }
}
