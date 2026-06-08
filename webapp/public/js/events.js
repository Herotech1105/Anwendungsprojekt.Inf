// events.js
import { logout } from "./auth.js";

/**
 * Liefert eine lokale ISO-ähnliche Zeichenkette ohne Zeitzone,
 * passend wenn das Backend lokale Timestamps erwartet.
 * Beispiel: "2024-06-03T19:30:00"
 */
function localInputToLocalIso(inputValue) {
    if (!inputValue) return null;
    // inputValue z.B. "2024-06-03T19:30" oder "2024-06-03T19:30:00"
    const [datePart, timePartRaw] = inputValue.split("T");
    if (!datePart || !timePartRaw) return null;
    const timePart = timePartRaw.length === 5 ? `${timePartRaw}:00` : timePartRaw;
    return `${datePart}T${timePart}`;
}

export function initEvents() {
    document.getElementById("loadDataBtn").addEventListener("click", () => {
        const fromLocal = document.getElementById("from").value; // "YYYY-MM-DDTHH:mm"
        const toLocal = document.getElementById("to").value;     // optional

        if (!fromLocal) {
            alert("Bitte Startzeit auswählen");
            return;
        }

        // Wir senden lokale Zeitstrings (Backend erwartet deutsche Lokalzeit)
        const from = localInputToLocalIso(fromLocal);
        const to = toLocal ? localInputToLocalIso(toLocal) : null;

        window.dispatchEvent(new CustomEvent("loadRange", { detail: { from, to } }));
    });

    document.getElementById("logoutBtn").addEventListener("click", () => {
        logout();
    });
}
