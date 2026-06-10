// js/frontend/auth.js
import { initEvents } from "./events.js";
import { initThemeToggle } from "./theme.js";

export let keycloak = null;

export function initAuth() {
    keycloak = new Keycloak({
        url: "https://local.kleber.data/auth",
        realm: "iot",
        clientId: "dashboard-client"
    });

    // Login wird erzwungen, bevor irgendwas anderes passiert
    keycloak.init({
        onLoad: "login-required",
        checkLoginIframe: false
    }).then(authenticated => {

        if (!authenticated) {
            // Falls aus irgendeinem Grund nicht eingeloggt → Login erzwingen
            keycloak.login();
            return;
        }

        updateUserInfo();

        // Events & Theme erst NACH erfolgreichem Login starten
        initEvents();
        initThemeToggle();

        // Token automatisch erneuern
        setInterval(() => {
            keycloak.updateToken(30).catch(() => keycloak.login());
        }, 20000);

    }).catch(err => {
        console.error("Keycloak Init Error:", err);
    });
}

export function logout() {
    keycloak.logout();
}

function updateUserInfo() {
    const el = document.getElementById("userInfo");
    if (!el) return;

    const name = keycloak.tokenParsed?.preferred_username || "Unbekannt";
    el.textContent = `Eingeloggt als: ${name}`;
}
