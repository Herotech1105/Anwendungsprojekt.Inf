// js/frontend/events.js
import { logout, keycloak } from "./auth.js";
import { exportDatabase } from "./api.js";

/*
   Robuste Rollen-Erkennung:
   - realm_access.roles
   - resource_access["dashboard-client"].roles
   - legacy realmAccess.roles
*/
function getUserRoles() {
    const t = keycloak.tokenParsed;

    const realmRoles =
        t?.realm_access?.roles || [];

    const clientRoles =
        t?.resource_access?.["dashboard-client"]?.roles || [];

    const legacyRealmRoles =
        keycloak.realmAccess?.roles || [];

    return [...new Set([
        ...realmRoles,
        ...clientRoles,
        ...legacyRealmRoles
    ])];
}

function isAdmin() {
    return getUserRoles().includes("admin-user");
}

export function initEvents() {

    document.getElementById("logoutBtn").addEventListener("click", logout);

    document.getElementById("loadDataBtn").addEventListener("click", () => {
        const from = document.getElementById("from").value;
        const to = document.getElementById("to").value || new Date().toISOString();

        if (!from) {
            alert("Bitte Startzeit auswählen");
            return;
        }

        window.dispatchEvent(new CustomEvent("loadRange", { detail: { from, to } }));
    });

    // --- Export Button Sichtbarkeit ---
    const exportBtn = document.getElementById("exportBtn");

    if (!isAdmin()) {
        exportBtn.style.display = "none";
    } else {
        exportBtn.style.display = "inline-block";
        exportBtn.addEventListener("click", exportDatabase);
    }

    // --- Range Buttons ---
    const rangeButtons = document.querySelectorAll(".range-btn");

    rangeButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            rangeButtons.forEach(b => b.classList.remove("active-range"));
            btn.classList.add("active-range");

            const hours = Number(btn.dataset.range);
            const to = new Date().toISOString();
            const from = new Date(Date.now() - hours * 3600 * 1000).toISOString();

            window.dispatchEvent(new CustomEvent("loadRange", { detail: { from, to } }));
        });
    });
}
