// js/frontend/events.js
import { logout, keycloak } from "./auth.js";
import { exportDatabase } from "./api.js";

export function initEvents() {

    // Logout
    document.getElementById("logoutBtn").addEventListener("click", logout);

    // Daten laden
    document.getElementById("loadDataBtn").addEventListener("click", () => {
        const from = document.getElementById("from").value;
        const to = document.getElementById("to").value || new Date().toISOString();

        if (!from) {
            alert("Bitte Startzeit auswählen");
            return;
        }

        window.dispatchEvent(new CustomEvent("loadRange", { detail: { from, to } }));
    });

    // Export nur für Admins
    document.getElementById("exportBtn").addEventListener("click", () => {
        const roles = keycloak.tokenParsed?.realm_access?.roles || [];

        if (!roles.includes("admin")) {
            alert("Nur Admins dürfen exportieren.");
            return;
        }

        exportDatabase();
    });

    // Range Buttons
    const rangeButtons = document.querySelectorAll(".range-btn");

    rangeButtons.forEach(btn => {
        btn.addEventListener("click", () => {

            // Aktiven Button markieren
            rangeButtons.forEach(b => b.classList.remove("active-range"));
            btn.classList.add("active-range");

            const hours = Number(btn.dataset.range);
            const to = new Date().toISOString();
            const from = new Date(Date.now() - hours * 3600 * 1000).toISOString();

            window.dispatchEvent(new CustomEvent("loadRange", { detail: { from, to } }));
        });
    });
}
