// frontend.js
const keycloak = new Keycloak({
  url: "https://www.lab.local/auth",
  realm: "iot",
  clientId: "dashboard-client",
});

let accessToken = null;

function initKeycloak() {
  keycloak
    .init({
      onLoad: "login-required",
      checkLoginIframe: false,
      pkceMethod: "S256",
    })
    .then((authenticated) => {
      if (!authenticated) {
        console.error("Nicht authentifiziert");
        keycloak.login();
      } else {
        accessToken = keycloak.token;
        console.log("Eingeloggt als:", keycloak.tokenParsed.preferred_username);

        // Token regelmäßig aktualisieren
        setInterval(() => {
          keycloak
            .updateToken(30)
            .then((refreshed) => {
              if (refreshed) {
                accessToken = keycloak.token;
              }
            })
            .catch(() => {
              console.error("Token-Refresh fehlgeschlagen");
              keycloak.login();
            });
        }, 20000);

        setupUi();
      }
    })
    .catch((err) => {
      console.error("Keycloak Init Fehler:", err);
    });
}

function setupUi() {
  const loadBtn = document.getElementById("loadDataBtn");
  loadBtn.addEventListener("click", () => {
    loadSensorData(false);
  });

  // Optional: initialer Live-Modus (ohne "to")
  loadSensorData(true);
}

async function loadSensorData(liveMode = false) {
  const fromInput = document.getElementById("from");
  const toInput = document.getElementById("to");

  const from = fromInput.value;
  const to = liveMode ? "" : toInput.value;

  if (!from) {
    alert("Bitte 'from' auswählen");
    return;
  }

  const params = new URLSearchParams();
  params.append("from", new Date(from).toISOString());
  if (to) {
    params.append("to", new Date(to).toISOString());
  }

  try {
    const res = await fetch(`/api/sensordata?${params.toString()}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (!res.ok) {
      console.error("Fehler beim Laden der Daten:", res.status);
      return;
    }

    const data = await res.json();
    updateChart(data);

    // Live-Modus: minütlich aktualisieren, wenn kein "to" gesetzt
    if (liveMode || !to) {
      setTimeout(() => loadSensorData(true), 60000);
    }
  } catch (err) {
    console.error("Fetch-Fehler:", err);
  }
}

document.addEventListener("DOMContentLoaded", initKeycloak);
