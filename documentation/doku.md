# Temperatur- und Luftfeuchtigkeitsregulierer

## Phasen (Patchnotes)

Die Präsentationen zu den einzelnen Phasen sind als PDF und Powerpoint/Google Presentation i Verzeichnis zu
finden.  
Im Folgenden sind die konkreten Änderungen während der einzelnen Phasen aufgegliedert

### Phase 1:

Datum: 11.04.2026 - 23.04.2026  
Problemstellung: Planung des Projektes und dessen 6 Phasen  
Verantwortlicher: Jannis Weber  
GANT-Diagramm: [Gantt_Phase1.pdf](Phase_1/Gantt_Phase1.pdf)

| Datei                                                    | Änderung | Erklärung                                                                           |
|----------------------------------------------------------|----------|-------------------------------------------------------------------------------------|
| [AnwendungInfoEli.pdf](Phase_1/AnwendungInfoEli.pdf)     | N/A      | Beschreibung der Anwendung und Projektidee mit Zielsetzung und Rahmenbedingungen    |
| [Machbarkeitstudie1.pdf](Phase_1/Machbarkeitstudie1.pdf) | N/A      | Machbarkeitsstudie zur technischen und wirtschaftlichen Umsetzbarkeit des Projektes |
| [6Phasen.png](Phase_1/6Phasen.png)                       | N/A      | Erstmalige Verteilung der ersten Phasen                                             |

### Phase 2:

Datum: 11.04.2026 - 28.04.2026
Problemstellung: Deployment der Kern-Infrastruktur
Verantwortlicher: Benjamin Hager
GANT-Diagramm:

| Datei | Änderung | Erklärung |
| --- | --- | --- |
| configurations/wlan_ap_setup.py | Neu erstellt, danach mehrfach überarbeitet (Firewall-Regeln korrigiert, SSH auf allen Interfaces erlaubt, Quellen ergänzt) | Python-Skript zur Einrichtung eines WLAN-Access-Points auf dem Raspberry Pi: konfiguriert hostapd, dnsmasq, statische IP (192.168.4.1), IP-Forwarding und nftables-Firewall mit NAT (Masquerading über eth0). Ermöglicht das Produktionsnetzwerk "Production" für IoT-Clients. |
| configurations/pico_main.py | Neu erstellt, danach erweitert (Phase 2 Integration) | MicroPython-Skript für den Raspberry Pi Pico W: verbindet sich als WLAN-Client mit dem Produktionsnetzwerk, ruft die Außentemperatur aus Friedrichshafen via Open-Meteo-API ab und steuert die Onboard-LED (Blinkrate abhängig von Temperatur: <10°C → 2s, ≤25°C → 1s, >25°C → 0.3s). |
| pico_wlan_connection.txt | Neu erstellt, danach angepasst | Dokumentation/Notizen zur WLAN-Konfiguration des Pico W (SSID, Passwort, Verbindungsaufbau). |

### Phase 3:

Datum: 
Problemstellung:  
Verantwortlicher:  
GANT-Diagramm:

| Datei | Änderung | Erklärung |
|-------|----------|-----------|

### Phase 4:

Datum: 06.05.2026 - 12.05.2026  
Problemstellung: Sichere Übermittlung der Sensordaten und Speicherung in der Datenbank  
Verantwortlicher: Lennart Esch  
GANT-Diagramm: ![GANT Diagramm Phase 4](./Phase_4/Phase_4_GANT.png)

| Datei                      | Änderung                                         | Erklärung                                                                                                                                                                                                                                                                                                                                                                                                                             |
|----------------------------|--------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| controller/config.py       | Neu                                              | Liest Environment Variablen aus der Dockerfile                                                                                                                                                                                                                                                                                                                                                                                        |
| controller/controller.py   | Neu                                              | Main Datei des controllers                                                                                                                                                                                                                                                                                                                                                                                                            |
| controller/Dockerfile      | Neu                                              | Dockerfile, um aus dem Controller ein Image zu bauen, enthält die definierten Environment Variablen                                                                                                                                                                                                                                                                                                                                   |
| controller/https_client.py | Neu                                              | Verwendet die Request Library um https requests zu schicken; wird verwendet für das Weiterleiten der Daten an nginx                                                                                                                                                                                                                                                                                                                   |
| controller/mqtt_handler.py | Neu                                              | Verwendet die paho_mqtt Library um beim mqtt-Broker zu subscriben, definiert ein Event, das ausgelöst wird wenn eine Nachricht vom Broker eingeht                                                                                                                                                                                                                                                                                     |
| controller/validation.py   | Neu                                              | Kontrolliert, ob die vom Broker erhaltene Nachricht valides JSON ist und prüft, ob die Werte plausibel sind (wird relevant, wenn der Pico angesteurt werden soll)                                                                                                                                                                                                                                                                     |
| nginx/nginx.conf           | Neu                                              | Konfiguration von nginx, reverse Proxy von https local.data.kleber zum webapp server und redirect von http auf https                                                                                                                                                                                                                                                                                                                  |
| webapp/Dockerfile          | Neu                                              | Dockerfile zum Bau eines Images für den webserver                                                                                                                                                                                                                                                                                                                                                                                     |
| webapp/package.json        | Neu                                              | Node Standard-Konfigurationsdatei für den webserver                                                                                                                                                                                                                                                                                                                                                                                   |
| webapp/package-lock.json   | Neu                                              | Node Standard-Konfigurationsdatei für den webserver                                                                                                                                                                                                                                                                                                                                                                                   |
| webapp/server.js           | Neu                                              | Controller + Service-Layer für den webserver, enthält POST-Endpunkt zum Empfangen von neuen Messdaten und anlegen neuer Messwerte in der Datenbank                                                                                                                                                                                                                                                                                    |
| webapp/config/database.js  | Neu                                              | Erzeugt einen Connection-Pool für den Datenbank Zugriff, der von ´server.js´ verwendet wird                                                                                                                                                                                                                                                                                                                                           |
| mariadb/01_tables.sql      | Neu                                              | Initialscript für die Datenbank; legt die Tabellen für Messwerte und Messwertarchiv an                                                                                                                                                                                                                                                                                                                                                |
| mariadb/02_archive_job.sql | Neu                                              | Initialscript für die Datenbank; legt den Archivierungsjob an; es werden täglich alle Daten, die älter als eine Woche sind von `sensor-data` zum `sensor-data-archive` verschoben                                                                                                                                                                                                                                                     |
| mariadb/03_user.sql        | Neu                                              | Initialscript für die Datenbank; legt einen Nutzer mit Schreibrechten für `sensor-data` an                                                                                                                                                                                                                                                                                                                                            |
| docker-compose.yml         | Konfiguration für die neuen Services hinzugefügt | Datenbank Konfiguration mit Health-Check und Verweiß auf die Entry Point Skripte hinzugefügt<br/>Nginx Configuration basierend auf dem OWASP Image hinzugefügt, enthält bereits Schutzmaßnahmen gegen Cross-Site-Scripting, SQL-Injektion und Directory Traversal<br/>Webapp Konfiguration basierend auf dem Image aus der Dockerfile hinzugefügt<br/>Controller Konfiguration basierend auf dem Image aus der Dockerfile hinzugefügt |

### Phase 5:

Datum: 13.05.2026 - 21.05.2026  
Problemstellung: Steuerung eines Aktors mittels LSTM-Neuronales Netz  
Verantwortlicher: Tim Dorozynski  
GANT-Diagramm: [GANT Diagramm Phase 5](./Phase_5/Phase_5_GANT.png)

| Datei                              | Änderung                                                  | Erklärung                                                                                                                                                                              |
|------------------------------------|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| controller/lstm_handler.py         | Neu                                                       | Lädt das trainierte LSTM-Modell und stellt Funktionen zur Verfügung, um Vorhersagen zu treffen; wird verwendet, um den optimalen Aktor-Wert basierend auf Sensor-Eingaben zu berechnen |
| controller/train.keras             | Neu                                                       | Trainiertes Keras/TensorFlow LSTM-Modell; Gewichte und Architektur für die Vorhersage des optimalen Regelwertes                                                                        |
| controller/train.py                | Neu                                                       | Trainingsscript für das LSTM-Modell; verwendet historische Messdaten um das Netz zu trainieren                                                                                         |
| controller/model_trainer.py        | Neu                                                       | Modulare Trainingsfunktionen für das LSTM-Modell; ermöglicht automatisches Retraining basierend auf neuen Daten                                                                        |
| controller/data_generation.py      | Neu                                                       | Generiert Trainingsdaten aus historischen Sensor-Messwerten; bereitet Daten für das LSTM-Training auf                                                                                  |
| controller/lstm_weights.weights.h5 | Neu                                                       | Exportierte Gewichte des trainierten LSTM-Modells; ermöglicht schnelleres Laden des Modells ohne Retraining                                                                            |
| configurations/pico/control.py     | Neu                                                       | Stellt Funktionen zur Ansteuerung des physischen Aktors (z.B. Heizung/Lüfter) bereit; implementiert PWM-Steuerung oder digitale Schaltausgänge                                         |
| configurations/pico/states.py      | Neu                                                       | Verwaltet die Zustände des Systems und des Aktors; definiert die möglichen Aktor-Positionen und deren Bedeutung                                                                        |
| docker-compose.yml                 | LSTM-Umgebungsvariablen im Controller-Service hinzugefügt | Ermöglicht Konfiguration des LSTM-Modells und Trainingparameter über Umgebungsvariablen; aktiviert LSTM-Vorhersagen im Controller                                                      |
| controller/Dockerfile              | TensorFlow/Keras Dependencies hinzugefügt                 | Integriert erforderliche Python-Libraries (tensorflow, keras, numpy, scikit-learn) für LSTM-Modellverarbeitung im Container                                                            |

### Phase 6:

Datum:  2026-05-22 bis 28
Problemstellung:  Sichere Web-Applikation (AuthN/AuthZ mit Keycloak)
Verantwortlicher:  Barnabas Steiner
GANT-Diagramm:

| Datei                                   | Änderung                                                                                                                    | Erklärung                                                                                                                    |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| docker-compose.yml                      | Service `keycloak_web` + Volume `keycloak_data` ergänzt, DB-Credentials in read/write getrennt, Healthchecks & `depends_on` | Integriert Keycloak als OIDC-Provider, hält dessen Daten persistent und sorgt für geordneten Startup der abhängigen Services |
| keycloak/iot-realm.json                 | Realm `iot` mit Rollen (`dashboard-user`, `admin-user`, `controller-ingest`), Benutzern und Clients angelegt                | Definiert die Sicherheitsdomäne: `dashboard-client` (Browser, PKCE) und `controller-client` (Maschine, Client-Credentials)   |
| nginx/nginx.conf                        | Route `/auth` auf Keycloak (Port 8443) + TLS-Zertifikatsprüfung, Trailing-Slash-Fix                                         | Macht Keycloak über den Reverse Proxy erreichbar und verschleiert das interne System                                         |
| mariadb/03_db_write_user.sql            | Aus `03_user.sql` umbenannt; Schreib-User `websrv_write` (INSERT, UPDATE)                                                   | Trennt schreibende DB-Zugriffe vom Lesen (Least Privilege)                                                                   |
| mariadb/06_db_read_user.sql             | Neuer Lese-User `websrv_read` mit `SELECT` auf `sensor_data`                                                                | Lese-APIs erhalten ausschließlich Leserechte                                                                                 |
| mariadb/05_training_data_privileges.sql | Privilegien an die Read/Write-Trennung angepasst                                                                            | Konsistente Rechtevergabe nach der User-Aufteilung                                                                           |
| webapp/config/database.js               | `getReadPool()` / `getWritePool()` statt einem `getPool()`                                                                  | Jeder Pool meldet sich mit eigenem DB-User an → Least Privilege auf Verbindungsebene                                         |
| webapp/server.js                        | JWKS-Client + Middleware `authenticateToken`; neuer Endpoint `GET /api/sensordata`                                          | Prüft das JWT (Signatur, Audience, Rolle `dashboard-user`); liefert Dashboard-Daten per JWT statt API-Key                    |
| webapp/package.json / package-lock.json | Dependencies `jwks-rsa` und `jsonwebtoken` ergänzt                                                                          | Bibliotheken zur serverseitigen Token-Validierung                                                                            |
| webapp/public/index.html                | Keycloak-Login-Redirect + Einbindung lokaler `keycloak.js`                                                                  | Leitet nicht angemeldete Nutzer zur Keycloak-Loginseite weiter                                                               |
| webapp/public/keycloak.js               | Neue lokale Kopie der Keycloak-JS-Bibliothek                                                                                | Auslieferung über die eigene App statt über eine externe Quelle                                                              |
| webapp/public/frontend.js               | Keycloak-Init + Sensordaten-Abruf per `fetch()` mit `Bearer`-Token                                                          | Initiiert AuthN/AuthZ und lädt Daten vom geschützten Endpoint                                                                |
| webapp/public/chart.js                  | Diagramm-Rendering + Live-Update implementiert                                                                              | Visualisiert Temperatur/Luftfeuchte, minütliche Aktualisierung                                                               |
| webapp/public/style.css                 | Styling-/Layout-Anpassungen                                                                                                 | Optische Gestaltung des Dashboards                                                                                           |
| webapp/Dockerfile                       | Aus Root-`Dockerfile` nach `webapp/` verschoben                                                                             | Trennt den Web-App-Build vom Projekt-Root                                                                                    |
| sensor-net/keycloak_auth.py             | Neu: Client-Credentials-Flow, Token-Cache, Rollenprüfung, Bearer-Header                                                     | Controller authentifiziert sich maschinell an Keycloak statt nur per API-Key                                                 |
| sensor-net/http_client.py               | `_build_headers()` (API-Key + Bearer); `verify=False` → `verify=CA_CERT_PATH`                                               | Zentrale Header-Erzeugung inkl. Token; echte TLS-Zertifikatsprüfung                                                          |
| sensor-net/controller.py                | `verify_role()` vor `warmstart()`; TLS-Verify aktiviert                                                                     | Beendet den Controller, wenn die geforderte Keycloak-Rolle fehlt                                                             |
| sensor-net/config.py                    | `KC_*`-Variablen (Token-URL, Client-ID/-Secret, Rolle) + `CA_CERT_PATH` ergänzt                                             | Konfigurierbare Keycloak-Parameter für den Controller                                                                        |
| sensor-net/Dockerfile                   | ENV-Defaults für die Keycloak-Variablen                                                                                     | Standardwerte für den Containerbetrieb                                                                                       |
| sensor-net/mqtt_handler.py              | Sendet Temperatur statt Prognose an `training_data`                                                                         | Korrigiert den an die Trainingsdaten übermittelten Wert                                                                      |
| configurations/wlan_ap_setup.py         | Backend unter eigenem Hostnamen im Produktions-WLAN                                                                         | Namensauflösung für den Zugriff auf das Backend                                                                              |

### Endspurt:

Liste mit übrigen Aufgaben

| Datei         | Änderung                                                                                                                                             | Erklärung                                                                                                                                            |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| CA/*          | Neugennerierung aller Zertifikate; Alle Zertifikate sind jetzt unter CA abgelegt                                                                     | Aufgrund von Schwierigkeiten bei den Zertifikaten wurden alle Zertifikate neu erstellt und befinden sich nun im CA Verzeichnis                       |
| environment/* | Environment Variablen wurden von der docker-compose und den Dockerfiles in dieses Verzeichnis nach dem Namensschema [container_name].env ausgelagert | Die Environment Dateien sind jetzt an einem Ort gebündelt und müssen bei Installation der Software angepasst werden, was hierdurch vereinfacht wurde |

## Projektstruktur

Erstellt mit MS-DOS `tree`

    Anwendungsprojekt.Inf
    │   docker-compose.yml
    │   README.md
    │
    ├───CA
    │       ca.crt
    │       ca.der
    │       ca.key
    │       ca.srl
    │       mqtt.crt
    │       mqtt.csr
    │       mqtt.key
    │       req.cnf
    │       www_cert.cert
    │       www_cert.csr
    │       www_key.key
    │
    ├───configurations
    │   │   wlan_ap_setup.py
    │   │
    │   ├───commands
    │   │       commands.txt
    │   │       san.cnf
    │   │
    │   └───pico
    │           control.py
    │           iot_config.py
    │           main.py
    │           mqtt.py
    │           states.py
    │           wifi.py
    │
    ├───controller
    │   │   config.py
    │   │   controller.py
    │   │   data_generation.py
    │   │   Dockerfile
    │   │   https_client.py
    │   │   keycloak_auth.py
    │   │   lstm_handler.py
    │   │   Messdaten.csv
    │   │   Messdaten2.csv
    │   │   model_trainer.py
    │   │   mqtt_handler.py
    │   │   requirements.txt
    │   │   train.keras
    │   │   train.py
    │   │   validation.py
    │   │   weather_data.csv
    │   │
    │   └───weights
    │          lstm_weights.weights.h5
    │   
    │
    ├───documentation
    │   │   doku.md
    │   │
    │   ├───Phase 1
    │   ├───Phase_1
    │   │       6Phasen.png
    │   │       AnwendungInfoEli.pdf
    │   │       Gantt_Phase1.pdf
    │   │       Machbarkeitstudie1.pdf
    │   │       Phase1.png
    │   │       Phase1_Praesentation.pdf
    │   │
    │   └───Phase_4
    │           API_Phase_4_Lennart_Esch.pdf
    │           API_Phase_4_Lennart_Esch.pptx
    │           Phase_4_GANT.png
    │           Phase_4_web_app_datenfluss.drawio.png
    │
    ├───environment
    │       controller.env
    │       db.env
    │       keycloak.env
    │       nginx.env
    │       webapp.env
    │
    ├───keycloak
    │   │   iot-realm.json
    │   │
    │   └───logs
    │           27.05.2026;13;00;00
    │
    ├───mariadb
    │       01_tables.sql
    │       02_archive_job.sql
    │       03_db_write_user.sql
    │       04_db_read_user.sql
    │       05_db_admin_user.sql
    │
    ├───mosquitto
    │   ├───config
    │   │       mosquitto.conf
    │   │
    │   ├───log
    │   │       mosquitto.log
    │   │
    │   └───secure
    │           acl
    │           pwfile
    │
    ├───nginx
    │       nginx.conf
    │
    ├───web-dashboard
    │   └───grafana
    │           dashboard.json
    │           prometheus.yml
    │
    └───webapp
    │   Dockerfile
    │   package-lock.json
    │   package.json
    │   server.js
    │
    ├───config
    │       database.js
    │
    ├───node_modules
    │
    ├───public
    │   │   index.html
    │   │   test.html
    │   │
    │   ├───css
    │   │       base.css
    │   │       components.css
    │   │       layout.css
    │   │       main.css
    │   │       status.css
    │   │       theme.css
    │   │
    │   ├───external
    │   │       chart.umd.js
    │   │       keycloak.js
    │   │
    │   ├───img
    │   │       LOGO.svg
    │   │
    │   └───js
    │           api.js
    │           auth.js
    │           chart-axes.js
    │           chart-colors.js
    │           chart-datasets.js
    │           chart-target-plugin.js
    │           chart-utils.js
    │           chart.js
    │           events.js
    │           main.js
    │           theme.js
    │
    └───service
            authentication.js
            validateSensorPayload.js

### Beschreibung der Komponenten (jeweils)

### CA

CA steht für Certificate authority. In diesem Verzeichnis liegen alle verwendeten Zertifikate. Alle verwendeten
Zertifikate sind selbstsigniert.

* `ca.crt`: Öffentliche Zertifikatsdatei, um die Zertifikate der Services zu verifizieren.
* `ca.der`: Öffentliche Zertifikatsdatei für den Pico in binärcode
* `ca.key`: Privater Schlüssel der CA zum signieren weiterer Zertifikate
* `ca.srl`: Serialisierungsnummer der `ca.crt`
* `commands.txt`: Befehle für das Generieren neuer Zertifikate
* `mqtt.crt`: Öffentliches Zertifikat für den mqtt-broker
* `mqtt.csr`: Certificate Signing Request; Zwischenschritt, um ein Zertifikat für den mqtt-broker zu signieren
* `mqtt.key`: Privater Schlüssel für den mqtt-broker
* `req.cnf`: Konfigurationsdatei für das Generieren und Signieren neuer Zertifikate
* `www_cert.cert`: Öffentliches Zertifikat für Nginx, Webserver und Keycloak
* `www_cert.csr`: Certificate Signing Request; Zwischenschritt, um ein Zertifikat für Nginx, Webserver und Keycloak zu
  signieren
* `www_key.key`: Privater Schlüssel für Nginx, Webserver und Keycloak

### configurations

Unter configurations sind alle Dateien abgelegt, die nicht für das Backend benötigt werden.  
Hier liegen das Script für den WLAN-Access-Point und unter pico die Dateien des Pico.

#### pico

#### wlan_ap_setup.py

### controller

Hier liegen alle Dateien für den Controller.

### webapp

#### config/database.js

In dieser Datei sind Pools für die jeweiligen Datenbanknutzer definiert.

#### service/authentication.js

Beinhaltet Middleware und Funktion für die Access Token Validierung

#### service/validateSensorPayload.js

Beinhaltet Funktion um Übertragunsinhalt der Sensoren (Temperatur, Luftfeuchtigkeit, Zeitstempel) zu validieren.
Gewährleistet, dass keine inkorekten Einträge in die Datenbank geschrieben werden.

#### server.js

Hauptkomponente des zum Starten des Webservers. Beinhaltet ebenfalls API für Lese- und Schreibzugriffe auf die Datenbank.


## Installation und Inbetriebnahme

Siehe `../README.md`

