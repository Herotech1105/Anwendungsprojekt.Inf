// js/frontend/events.js
import { logout, keycloak } from "./auth.js";
import { exportDatabase } from "./api.js";

function isAdmin() {
    const rolesFromToken = keycloak.tokenParsed?.realm_access?.roles || [];
    const rolesFromRealm = keycloak.realmAccess?.roles || [];
    const roles = [...new Set([...rolesFromToken, ...rolesFromRealm])];
    return roles.includes("admin");
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

    const exportBtn = document.getElementById("exportBtn");

    if (!isAdmin()) {
        exportBtn.style.display = "none";
    } else {
        exportBtn.style.display = "inline-block";
        exportBtn.addEventListener("click", () => {
            exportDatabase();
        });
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
