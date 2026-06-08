import { logout } from "./auth.js";

function localToUTC(inputValue) {
    const d = new Date(inputValue);

    return new Date(
        Date.UTC(
            d.getFullYear(),
            d.getMonth(),
            d.getDate(),
            d.getHours(),
            d.getMinutes(),
            d.getSeconds()
        )
    ).toISOString();
}

export function initEvents() {
    document.getElementById("loadDataBtn").addEventListener("click", () => {
        const fromLocal = document.getElementById("from").value;
        const toLocal = document.getElementById("to").value;

        if (!fromLocal) {
            alert("Bitte Startzeit auswählen");
            return;
        }

        const from = localToUTC(fromLocal);
        const to = toLocal ? localToUTC(toLocal) : null;

        window.dispatchEvent(new CustomEvent("loadRange", { detail: { from, to } }));
    });

    document.getElementById("logoutBtn").addEventListener("click", () => {
        logout();
    });
}
