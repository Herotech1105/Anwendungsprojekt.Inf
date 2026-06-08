# Temperatur- und Luftfeuchtigkeitsregulierer

## Phasen (Patchnotes)

Die Präsentationen zu den einzelnen Phasen sind als PDF und Powerpoint/Google Presentation im gleichen Verzeichnis zu
finden.  
Im Folgenden sind die konkreten Änderungen während der einzelnen Phasen aufgegliedert

### Phase 1:

Datum:   
Problemstellung:  
Verantwortlicher:  
GANT-Diagramm:

| Datei | Änderung | Erklärung |
|-------|----------|-----------|

### Phase 2:

Datum:  
Problemstellung:  
Verantwortlicher:  
GANT-Diagramm:

| Datei | Änderung | Erklärung |
|-------|----------|-----------|

### Phase 3:

Datum:  
Problemstellung:  
Verantwortlicher:  
GANT-Diagramm:

| Datei | Änderung | Erklärung |
|-------|----------|-----------|

### Phase 4:

Datum:  
Problemstellung:  
Verantwortlicher:  
GANT-Diagramm:

| Datei                        | Änderung                                          | Erklärung                                                                                                                                                         |
|------------------------------|---------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| controller/config.py         | Neu                                               | Liest Environment Variablen aus der Dockerfile                                                                                                                    |
| controller/controller.py     | Neu                                               | Main Datei des controllers                                                                                                                                        |
| controller/Dockerfile        | Neu                                               | Dockerfile, um aus dem Controller ein Image zu bauen, enthält die definierten Environment Variablen                                                               |
| controller/https_client.py   | Neu                                               | Verwendet die Request Library um https requests zu schicken; wird verwendet für das Weiterleiten der Daten an nginx                                               |
| controller/mqtt_handler.py   | Neu                                               | Verwendet die paho_mqtt Library um beim mqtt-Broker zu subscriben, definiert ein Event, das ausgelöst wird wenn eine Nachricht vom Broker eingeht                 |
| controller/validation.py     | Neu                                               | Kontrolliert, ob die vom Broker erhaltene Nachricht valides JSON ist und prüft, ob die Werte plausibel sind (wird relevant, wenn der Pico angesteurt werden soll) |
| nginx/nginx.conf             | Neu                                               | Konfiguration von nginx                                                                                                                                           |
| webapp/Dockerfile            | Neu                                               |                                                                                                                                                                   |
| webapp/package.json          | Neu                                               |                                                                                                                                                                   |
| webapp/package-lock.json     | Neu                                               |                                                                                                                                                                   |
| webapp/server.js             | Neu                                               |                                                                                                                                                                   |
| webapp/config/database.js    | Neu                                               |                                                                                                                                                                   |
| mariadb/01_tables.sql        | Neu                                               |                                                                                                                                                                   |
| mariadb/02_archive_job.sql   | Neu                                               |                                                                                                                                                                   |
| mariadb/03_db_write_user.sql | Neu                                               |                                                                                                                                                                   |
| docker-compose.yml           | Konfiguration für die neuene Services hinzugefügt |                                                                                                                                                                   |

### Phase 5:

Datum:  
Problemstellung:  
Verantwortlicher:
GANT-Diagramm:

| Datei | Änderung | Erklärung |
|-------|----------|-----------|

### Phase 6:

Datum:  2026-05-22 bis 28
Problemstellung:  Sichere Web-Applikation (AuthN/AuthZ mit Keycloak)
Verantwortlicher:  Barnabas Steiner
GANT-Diagramm:

| Datei | Änderung | Erklärung |
|-------|----------|-----------|
| docker-compose.yml | Service `keycloak_web` + Volume `keycloak_data` ergänzt, DB-Credentials in read/write getrennt, Healthchecks & `depends_on` | Integriert Keycloak als OIDC-Provider, hält dessen Daten persistent und sorgt für geordneten Startup der abhängigen Services |
| keycloak/iot-realm.json | Realm `iot` mit Rollen (`dashboard-user`, `admin-user`, `controller-ingest`), Benutzern und Clients angelegt | Definiert die Sicherheitsdomäne: `dashboard-client` (Browser, PKCE) und `controller-client` (Maschine, Client-Credentials) |
| nginx/nginx.conf | Route `/auth` auf Keycloak (Port 8443) + TLS-Zertifikatsprüfung, Trailing-Slash-Fix | Macht Keycloak über den Reverse Proxy erreichbar und verschleiert das interne System |
| mariadb/03_db_write_user.sql | Aus `03_user.sql` umbenannt; Schreib-User `websrv_write` (INSERT, UPDATE) | Trennt schreibende DB-Zugriffe vom Lesen (Least Privilege) |
| mariadb/06_db_read_user.sql | Neuer Lese-User `websrv_read` mit `SELECT` auf `sensor_data` | Lese-APIs erhalten ausschließlich Leserechte |
| mariadb/05_training_data_privileges.sql | Privilegien an die Read/Write-Trennung angepasst | Konsistente Rechtevergabe nach der User-Aufteilung |
| webapp/config/database.js | `getReadPool()` / `getWritePool()` statt einem `getPool()` | Jeder Pool meldet sich mit eigenem DB-User an → Least Privilege auf Verbindungsebene |
| webapp/server.js | JWKS-Client + Middleware `authenticateToken`; neuer Endpoint `GET /api/sensordata` | Prüft das JWT (Signatur, Audience, Rolle `dashboard-user`); liefert Dashboard-Daten per JWT statt API-Key |
| webapp/package.json / package-lock.json | Dependencies `jwks-rsa` und `jsonwebtoken` ergänzt | Bibliotheken zur serverseitigen Token-Validierung |
| webapp/public/index.html | Keycloak-Login-Redirect + Einbindung lokaler `keycloak.js` | Leitet nicht angemeldete Nutzer zur Keycloak-Loginseite weiter |
| webapp/public/keycloak.js | Neue lokale Kopie der Keycloak-JS-Bibliothek | Auslieferung über die eigene App statt über eine externe Quelle |
| webapp/public/frontend.js | Keycloak-Init + Sensordaten-Abruf per `fetch()` mit `Bearer`-Token | Initiiert AuthN/AuthZ und lädt Daten vom geschützten Endpoint |
| webapp/public/chart.js | Diagramm-Rendering + Live-Update implementiert | Visualisiert Temperatur/Luftfeuchte, minütliche Aktualisierung |
| webapp/public/style.css | Styling-/Layout-Anpassungen | Optische Gestaltung des Dashboards |
| webapp/Dockerfile | Aus Root-`Dockerfile` nach `webapp/` verschoben | Trennt den Web-App-Build vom Projekt-Root |
| sensor-net/keycloak_auth.py | Neu: Client-Credentials-Flow, Token-Cache, Rollenprüfung, Bearer-Header | Controller authentifiziert sich maschinell an Keycloak statt nur per API-Key |
| sensor-net/http_client.py | `_build_headers()` (API-Key + Bearer); `verify=False` → `verify=CA_CERT_PATH` | Zentrale Header-Erzeugung inkl. Token; echte TLS-Zertifikatsprüfung |
| sensor-net/controller.py | `verify_role()` vor `warmstart()`; TLS-Verify aktiviert | Beendet den Controller, wenn die geforderte Keycloak-Rolle fehlt |
| sensor-net/config.py | `KC_*`-Variablen (Token-URL, Client-ID/-Secret, Rolle) + `CA_CERT_PATH` ergänzt | Konfigurierbare Keycloak-Parameter für den Controller |
| sensor-net/Dockerfile | ENV-Defaults für die Keycloak-Variablen | Standardwerte für den Containerbetrieb |
| sensor-net/mqtt_handler.py | Sendet Temperatur statt Prognose an `training_data` | Korrigiert den an die Trainingsdaten übermittelten Wert |
| configurations/wlan_ap_setup.py | Backend unter eigenem Hostnamen im Produktions-WLAN | Namensauflösung für den Zugriff auf das Backend |

### Endspurt:

Liste mit übrigen Aufgaben

| Datei | Änderung | Erklärung |
|-------|----------|-----------|

## Projektstruktur

`
Verzeichnismodell
`

Beschreibung

### Beschreibung der Komponenten (jeweils)

## Installation und Inbetriebnahme

Siehe `../README.md`

