// auth.js
const Keycloak = window.Keycloak;

export const keycloak = new Keycloak({
    url: "https://local.kleber.data/auth",
    realm: "iot",
    clientId: "dashboard-client"
});

export async function initAuth() {
    try {
        const authenticated = await keycloak.init({
            onLoad: "login-required",
            checkLoginIframe: false
        });

        if (!authenticated) {
            console.error("User not authenticated");
            return;
        }

        console.debug("[auth] authenticated user", keycloak.tokenParsed && keycloak.tokenParsed.preferred_username);

        const userInfoEl = document.getElementById("userInfo");
        if (userInfoEl) userInfoEl.textContent = "Eingeloggt als: " + keycloak.tokenParsed.preferred_username;

        setInterval(() => {
            keycloak.updateToken(30).catch(() => {
                console.error("Token refresh failed");
                keycloak.login();
            });
        }, 30000);

    } catch (err) {
        console.error("Keycloak init error:", err);
    }
}

export function logout() {
    console.debug("[auth] logout called");
    keycloak.logout();
}
