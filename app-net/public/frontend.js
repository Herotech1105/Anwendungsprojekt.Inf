const keycloak = new Keycloak({
    url: "https://www.lab.local/auth",
    realm: "iot",
    clientId: "dashboard-client"
});

async function initAuth() {
    try {
        const authenticated = await keycloak.init({
            onLoad: "login-required",
            checkLoginIframe: false
        });

        if (!authenticated) {
            console.error("User not authenticated");
            return;
        }

        document.getElementById("userInfo").textContent =
            "Eingeloggt als: " + keycloak.tokenParsed.preferred_username;

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

async function apiGet(path) {
    const url = `https://www.lab.local/api${path}`;

    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + keycloak.token
        }
    });

    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }

    return response.json();
}

export async function getSensorRange(from, to) {
    const query = `?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}`;
    return apiGet(`/sensordata/range${query}`);
}

document.getElementById("loadDataBtn").addEventListener("click", () => {
    const from = document.getElementById("from").value;
    const to = document.getElementById("to").value;

    if (!from) {
        alert("Bitte Startzeit auswählen");
        return;
    }

    window.dispatchEvent(new CustomEvent("loadRange", { detail: { from, to } }));
});

// --- Dark Mode Toggle (ohne Speicherung) ---
const themeToggle = document.getElementById("themeToggle");

themeToggle.addEventListener("change", () => {
    if (themeToggle.checked) {
        document.body.classList.add("dark");
    } else {
        document.body.classList.remove("dark");
    }
});

// --- Logout Button ---
document.getElementById("logoutBtn").addEventListener("click", () => {
    keycloak.logout();
});

initAuth();
