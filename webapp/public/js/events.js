import { logout } from "./auth.js";

export function initEvents() {
    document.getElementById("loadDataBtn").addEventListener("click", () => {
        const from = document.getElementById("from").value;
        const to = document.getElementById("to").value;

        if (!from) {
            alert("Bitte Startzeit auswählen");
            return;
        }

        window.dispatchEvent(new CustomEvent("loadRange", { detail: { from, to } }));
    });

    document.getElementById("logoutBtn").addEventListener("click", () => {
        logout();
    });
}
