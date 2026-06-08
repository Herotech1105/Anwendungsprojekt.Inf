// events.js
import { logout } from "./auth.js";

function localInputToLocalIso(inputValue) {
    if (!inputValue) return null;
    const [datePart, timePartRaw] = inputValue.split("T");
    if (!datePart || !timePartRaw) return null;
    const timePart = timePartRaw.length === 5 ? `${timePartRaw}:00` : timePartRaw;
    return `${datePart}T${timePart}`;
}

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

            const fromMs = localInputToMs(fromLocal);
            const toMs = toLocal ? localInputToMs(toLocal) : null;

            const fromIsoLocal = localInputToLocalIso(fromLocal);
            const toIsoLocal = toLocal ? localInputToLocalIso(toLocal) : null;

            console.debug("[events] user selected", { fromLocal, toLocal, fromMs, toMs, fromIsoLocal, toIsoLocal });

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
