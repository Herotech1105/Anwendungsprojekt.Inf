import { logout } from "./auth.js";

/**
 * Convert a datetime-local input value (e.g. "2024-06-03T19:30")
 * into an ISO Z string that represents the same clock time in UTC:
 * "2024-06-03T19:30:00.000Z"
 *
 * This avoids any browser-local-to-UTC shifting caused by new Date(...).toISOString()
 */
function localInputToUTCIso(inputValue) {
    if (!inputValue) return null;

    // inputValue is typically "YYYY-MM-DDTHH:mm" or "YYYY-MM-DDTHH:mm:ss"
    const [datePart, timePartRaw] = inputValue.split("T");
    if (!datePart || !timePartRaw) return null;

    // Ensure seconds exist
    const timePart = timePartRaw.length === 5 ? `${timePartRaw}:00` : timePartRaw;

    // Return ISO Z string that treats the chosen clock time as UTC
    return `${datePart}T${timePart}.000Z`;
}

export function initEvents() {
    document.getElementById("loadDataBtn").addEventListener("click", () => {
        const fromLocal = document.getElementById("from").value;
        const toLocal = document.getElementById("to").value;

        if (!fromLocal) {
            alert("Bitte Startzeit auswählen");
            return;
        }

        // Convert the datetime-local input into an ISO Z string that represents the same clock time in UTC
        const from = localInputToUTCIso(fromLocal);
        const to = toLocal ? localInputToUTCIso(toLocal) : null;

        window.dispatchEvent(new CustomEvent("loadRange", { detail: { from, to } }));
    });

    document.getElementById("logoutBtn").addEventListener("click", () => {
        logout();
    });
}
