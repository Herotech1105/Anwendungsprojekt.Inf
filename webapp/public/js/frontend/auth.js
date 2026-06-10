// js/frontend/auth.js
export let keycloak = null;

export function initAuth() {
    keycloak = new Keycloak({
        url: "https://auth.kleber.data/",
        realm: "iot",
        clientId: "iot-frontend"
    });

    keycloak.init({ onLoad: "login-required" }).then(() => {
        updateUserInfo();
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
