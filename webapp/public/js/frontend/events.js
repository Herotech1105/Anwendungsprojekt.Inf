// js/frontend/events.js
import { logout, keycloak } from "./auth.js";
import { exportDatabase } from "./api.js";

/*
* Gets the User roles from the keycloak token
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

/*
* Checks if a user is an admin user
*/
function isAdmin() {
    return getUserRoles().includes("admin-user");
}

/*
* Event-Handling for Buttons
*/
export function initEvents() {

    document.getElementById("logoutBtn").addEventListener("click", logout);

    document.getElementById("loadDataBtn").addEventListener("click", () => {
        const fromDate = document.getElementById("from").value;
        const toDate = document.getElementById("to").value;

        if (!fromDate) {
            alert("Bitte Startdatum auswählen");
            return;
        }

        const from = fromDate + "T00:00:00";
        const to = toDate ? toDate + "T23:59:59" : new Date().toISOString();

        window.dispatchEvent(new CustomEvent("loadRange", { detail: { from, to } }));
    });

    const exportBtn = document.getElementById("exportBtn");

    if (!isAdmin()) {
        exportBtn.style.display = "none";
    } else {
        exportBtn.style.display = "inline-block";
        exportBtn.addEventListener("click", exportDatabase);
    }

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
