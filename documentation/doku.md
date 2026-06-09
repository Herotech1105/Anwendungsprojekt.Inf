# Temperatur- und Luftfeuchtigkeitsregulierer

In diesem Projekt wurde ein Regulierungssystem für Luftfeuchtigkeit und Temperatur entwickelt, dass die Messdaten sicher
speichert und für einen authentifizierten Nutzer die Messdaten der letzten Woche visualisiert.  
Die Anforderungen für das Endprodukt waren die folgenden:

*
*

Zur Erarbeitung des
Projekts wurde dieses in die folgenden 6 Phasen eingeteilt:

1. Planung und Einteilung der folgenden Phasen
2. Erstellen eines WLAN Access Points mit Firewall
3. Verdrahtung des Pico und Übertragen der Sensordaten an das Backend
4. Sicheres Speichern der Sensordaten in der Datenbank
5. Steuerung der Aktoren des Pico mittels LSTM-Netz
6. Erstellen einer sicheren Web Applikation für die Sensordaten

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
![GANT Diagramm Phase 2](./Phase_2/phase-2-gantt.svg)  

| Datei                           | Änderung                                                                                                                   | Erklärung                                                                                                                                                                                                                                                                             |
|---------------------------------|----------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| configurations/wlan_ap_setup.py | Neu erstellt, danach mehrfach überarbeitet (Firewall-Regeln korrigiert, SSH auf allen Interfaces erlaubt, Quellen ergänzt) | Python-Skript zur Einrichtung eines WLAN-Access-Points auf dem Raspberry Pi: konfiguriert hostapd, dnsmasq, statische IP (192.168.4.1), IP-Forwarding und nftables-Firewall mit NAT (Masquerading über eth0). Ermöglicht das Produktionsnetzwerk "Production" für IoT-Clients.        |
| configurations/pico_main.py     | Neu erstellt, danach erweitert (Phase 2 Integration)                                                                       | MicroPython-Skript für den Raspberry Pi Pico W: verbindet sich als WLAN-Client mit dem Produktionsnetzwerk, ruft die Außentemperatur aus Friedrichshafen via Open-Meteo-API ab und steuert die Onboard-LED (Blinkrate abhängig von Temperatur: <10°C → 2s, ≤25°C → 1s, >25°C → 0.3s). |
| pico_wlan_connection.txt        | Neu erstellt, danach angepasst                                                                                             | Dokumentation/Notizen zur WLAN-Konfiguration des Pico W (SSID, Passwort, Verbindungsaufbau).                                                                                                                                                                                          |

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
GANT-Diagramm:
![GANT Diagramm Phase 4](./Phase_4/Phase_4_GANT.png)

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
GANT-Diagramm:
[GANT Diagramm Phase 5](./Phase_5/Phase_5_GANT.png)

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

Datum:  22.05.2026 - 28.05.2026
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
    │       (Zertifikate und Dateien zum anlegen)
    │
    ├───configurations
    │   │   wlan_ap_setup.py
    │   │
    │   └───pico
    │           (Dateien des Pico)
    │
    ├───controller
    │   │   (Hauptdateien des Controller)
    │   │
    │   └───weights
    │          (Gewichte für das LSTM-Netzwerk)
    │   
    │
    ├───documentation
    │       (Dokumentation)
    │
    ├───environment
    │       (Dateien für die Umgebungsvariablen der einzelnen Services)
    │
    ├───keycloak
    │   └───iot-realm.json
    │
    ├───mariadb
    │       (Initialisierungsskripte für die Datenbank)
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
    └───webapp
         │   (Hauptdateien für den Webserver)
         │
         └───public
                 (Öffentliche Dateien für den Client)

## Deployment Diagramm

## Beschreibung der Komponenten

### CA

CA steht für Certificate authority. In diesem Verzeichnis liegen alle verwendeten Zertifikate. Alle verwendeten
Zertifikate sind selbstsigniert.

### configurations

Unter configurations sind alle Dateien abgelegt, die nicht für das Backend benötigt werden.  
Hier liegen das Script für den WLAN-Access-Point und unter pico die Dateien des Pico.

#### pico

#### wlan_ap_setup.py

### controller

Der Controller ist die zentrale Brücke zwischen dem **Sensor-Netzwerk** und dem **Backend-Server**. Er läuft als
eigenständiger Docker-Container im `sensor-network` und hat zwei Hauptaufgaben:

1. **Sensordaten empfangen und weiterleiten**  
   Der Controller abonniert das MQTT-Topic `sensor/data`, auf dem der Raspberry Pi Pico Temperatur- und
   Feuchtigkeitsmesswerte publiziert. Jede eingehende Nachricht wird validiert und per HTTPS an den Backend-Webserver (
   `server.js`) hinter dem nginx Reverse Proxy weitergeleitet, der sie in der MariaDB-Datenbank speichert.

2. **Steuerungsentscheidungen treffen**  
   Mithilfe eines LSTM-Modells erstellt der Controller eine Vorhersage der nächsten Temperatur- und Feuchtigkeitswerte.
   Basierend auf dieser Vorhersage und konfigurierbaren Schwellenwerten wird eine Aktor-Steuerungsnachricht (`COOL`,
   `HEAT`, `DRY`, `HUM` oder `OK`) auf dem MQTT-Topic `actuator/control` publiziert, die der Pico empfängt und umsetzt.

Der Controller authentifiziert sich per **Keycloak Client Credentials Flow** mit einem OAuth2 Access-Token und sendet
dieses als `Authorization: Bearer`-Header bei jedem Request an das Backend mit. Beim Start wird geprüft, ob das Token
die Rolle `controller-ingest` enthält — ist dies nicht der Fall, beendet sich der Controller.

Die gesamte Kommunikation erfolgt verschlüsselt: MQTT über TLS (Port 8883) und HTTP über HTTPS (Port 443), wobei die
Zertifikate gegen die Projekt-CA validiert werden.

#### `config.py`

Zentrale Konfigurationsdatei des Controllers. Liest alle Betriebsparameter aus Environment-Variablen aus, die im
Dockerfile definiert und optional über `docker-compose.yml` überschrieben werden. Dazu gehören:

- **MQTT-Verbindungsdaten** — Host, Port, Benutzer, Passwort, Topic
- **Backend-Konfiguration** — URL, API-Key, HTTP-Timeout
- **Keycloak-Zugangsdaten** — Client-ID, Client-Secret, Token-URL, benötigte Rolle
- **TLS** — Pfad zum CA-Zertifikat
- **Plausibilitätsgrenzen** — Min/Max für Temperatur und Luftfeuchtigkeit
- **Steuerungsschwellenwerte** — Ober-/Untergrenzen für die Aktor-Kontrolle

Außerdem wird hier das zentrale Logging konfiguriert, das von allen anderen Modulen über den `log`-Logger verwendet
wird.

#### `controller.py`

Einstiegspunkt und Main-Datei des Controllers. Der Ablauf beim Start:

1. Environment-Variablen auf Vollständigkeit prüfen (API-Key, MQTT-Passwort, CA-Datei)
2. **Keycloak-Authentifizierung** — Access-Token holen und Rolle `controller-ingest` verifizieren. Schlägt dies fehl,
   beendet sich der Controller sofort.
3. MQTT-Client aufbauen
4. Endlosschleife (`loop_forever`) starten, die Reconnects bei Verbindungsabbrüchen automatisch handhabt

Signal-Handler für `SIGTERM` und `SIGINT` sorgen für ein sauberes Herunterfahren bei `docker stop`.

#### `keycloak_auth.py`

Zuständig für die gesamte Keycloak-Authentifizierung per **OAuth2 Client Credentials Flow**.

| Funktion          | Beschreibung                                                                                                                               |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `request_token()` | POST-Request an den Keycloak-Token-Endpoint mit `client_id` und `client_secret`. Empfängt das Access-Token (JWT) und cached es im Speicher |
| `get_token()`     | Gibt ein gültiges Token zurück — cached oder neu geholt. Erneuert automatisch 30 Sekunden vor Ablauf                                       |
| `verify_role()`   | Dekodiert den JWT-Payload per Base64 und prüft, ob `controller-ingest` im Feld `realm_access.roles` vorhanden ist                          |
| `auth_header()`   | Liefert einen fertigen `Authorization: Bearer <token>`-Header für HTTP-Requests                                                            |

#### `mqtt_handler.py`

Baut den MQTT-Client auf und definiert die drei Callback-Funktionen für die paho-mqtt-Bibliothek (v2 API).

| Callback        | Beschreibung                                             |
|-----------------|----------------------------------------------------------|
| `on_connect`    | Abonniert das Sensor-Topic nach erfolgreicher Verbindung |
| `on_disconnect` | Loggt den Verbindungsabbruch                             |
| `on_message`    | Zentrale Verarbeitungslogik (siehe unten)                |

**Ablauf bei eingehender Nachricht (`on_message`):**

1. Nachricht durch `validation.py` validieren
2. UTC-Timestamp setzen
3. Daten per `https_client.py` an das Backend weiterleiten
4. LSTM-Vorhersage abrufen
5. Steuerungsentscheidung treffen (`COOL` / `HEAT` / `DRY` / `HUM` / `OK`)
6. Ergebnis auf `actuator/control` publizieren

Enthält zusätzlich die Hilfsfunktionen `_determine_temp_state()`, `_determine_hum_state()` und `_resolve_action()` für
die Schwellenwert-Logik, sowie `build_client()` für den TLS-gesicherten Client-Aufbau.

#### `https_client.py`

Zuständig für die HTTP-Weiterleitung der Sensordaten an das Backend.

| Funktion               | Beschreibung                                                                                   |
|------------------------|------------------------------------------------------------------------------------------------|
| `_build_headers()`     | Erstellt die HTTP-Header mit API-Key (`x-api-key`) und Keycloak Bearer-Token (`Authorization`) |
| `forward_to_backend()` | HTTPS-POST mit Sensor-Payload (Temperatur, Feuchtigkeit, Timestamp) an die Backend-URL         |

Die TLS-Verbindung wird gegen das CA-Zertifikat validiert. Fehler werden abgefangen und geloggt, ohne eine Exception zu
werfen, damit der MQTT-Loop nicht unterbrochen wird.

#### `validation.py`

Validiert jede eingehende MQTT-Nachricht in drei Schritten:

1. **JSON-Prüfung** — Ist der Payload gültiges JSON und ein Objekt?
2. **Feld-Extraktion** — Sind `temperature` und `humidity` als Zahlenwerte vorhanden?
3. **Range-Check** — Liegen die Werte innerhalb der konfigurierbaren Plausibilitätsgrenzen? (Standard: 0–100)

Nur wenn alle drei Prüfungen bestanden sind, werden die Werte als Tuple zurückgegeben. Andernfalls wird `None`
zurückgegeben und eine Warnung geloggt. Dies schützt die Pipeline vor fehlerhaften oder manipulierten Nachrichten.

#### `lstm_handler.py`

Lädt beim Start das trainierte LSTM-Keras-Modell (`train.keras`) und verwaltet einen Ringbuffer der letzten 10
Messwerte.

| Funktion               | Beschreibung                                                                                                                                                                           |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `predict_next_value()` | Fügt einen neuen Messwert zum Buffer hinzu. Sobald 10 Werte vorhanden sind: Normalisierung → Modell-Vorhersage → Rückskalierung. Gibt vorhergesagte Temperatur und Feuchtigkeit zurück |

Der MinMaxScaler wird manuell mit den gleichen Parametern wie im Training konfiguriert (Bereich 0–100 für beide
Features).

#### `model_trainer.py`

Trainingsscript für das LSTM-Modell.

- **Input:** CSV-Datei (`weather_data.csv`) mit Temperatur- und Feuchtigkeitswerten
- **Preprocessing:** MinMaxScaler (0–1), Sliding-Window-Sequenzen der Länge 10
- **Architektur:** LSTM (64 Units) → Dense (32 Units) → Dense (2 Outputs: Temperatur, Feuchtigkeit)
- **Training:** Adam-Optimizer, MSE-Loss, 15 Epochen, Batch-Size 32
- **Output:** Gespeichertes Modell als `train.keras`

#### `data_generation.py`

Generiert synthetische Trainingsdaten für das LSTM-Modell.

- **Umfang:** 30 Tage im Minutentakt (43.200 Datenpunkte)
- **Simulation:** Sinusförmige Tag-/Nacht-Zyklen, Zufallsrauschen, simulierte Thermostat-Logik (Heizung/Kühlung)
- **Output:** `weather_data.csv` als Input für `model_trainer.py`

#### `train.py`

Alternatives Trainingsscript mit einer anderen Modellarchitektur (zwei gestapelte LSTM-Schichten mit Dropout statt einer
einzelnen). Nutzt synthetisch generierte Sinus-Daten statt einer CSV-Datei und gibt nur einen Wert aus. Dient als
früherer Prototyp — das produktive Training erfolgt über `model_trainer.py`.

### webapp

#### config/database.js

In dieser Datei sind Pools für die jeweiligen Datenbanknutzer definiert.
Hier speziell für den Read-, Write- und Adminuser.

#### public

Dieser Ordner beinhaltet alle Frontendelemente für das Anzeigen des Dashboardes.

- **css** — Verwendete CSS-Elemente
- **external** — Extern importierte Skripte
- **img** — Bilddateien
- **js** — Verwendete Skripte
- **index.html** — HTML-Element für das Dashboard

#### service/authentication.js

Beinhaltet Middleware und Funktion für die Access Token Validierung
Speziell geprüft wird das Vorhandensein des Tokens und die erwarteten Audiences und Rollen.
Darüberhinaus ist der Endpoint für die Authentifizierung des API-Keys für die Datenbankzugriffe definiert.

#### service/validateSensorPayload.js

Beinhaltet Funktion um Übertragunsinhalt der Sensoren (Temperatur, Luftfeuchtigkeit, Zeitstempel) zu validieren.
Es wird speziell geprüft:

1. Sind Temperatur und Luftfeuchtigkeit als Zahlen vertreten
2. Ist das Format des Zeitstempels valide
3. Sind Temperatur und Luftfeuchtigkeit innerhalb des definierten Bereiches
4. Ist der Zeitstempel aktuell

Damit werden korrekte Einträge in der Datenbank gewährleistet.

#### server.js

Hauptkomponente des zum Starten des Webservers. Beinhaltet ebenfalls API für Lese- und Schreibzugriffe auf die Datenbank.
Gegebene Endpoints:

- **GET /api/status** — Serverstatus abfragen
- **GET /api/sensordata** — Aktuellste Sensordaten erhalten
- **GET /api/sensordata/range** — Sensordaten von einem bestimmten Zeitfenster erhalten
- **GET /api/admin/export** — Aktuelle und Archivierte Sensordaten als CSV erhalten
- **POST /api/internal/sensordata** — Sensordaten in Datenbank schreiben

## Installation und Inbetriebnahme

### Pi Setup

* Installiere das Raspberry Pi light Image auf beiden Pis
* Lies die MAC-Addresse eines Pis aus; dieser Pi wird später zum Backend

### WLAN AP

* Verbinde den WLAN Pi über ein Netzwerkkabel mit dem Internet
* Stelle eine Verbindung zum Pi via ssh her
* Setze backend_mac_address in Zeile 4 in `/conficuration/wlan_ap_setup.py` auf die MAC-Addresse des Backends
* Bei Bedarf können auch Passwort und SSID in den zwei folgenden Zeilen geändert werden
* Führe `sudo apt install hostapd dnsmasq` auf dem Pi aus
* Kopiere jetzt das Skript `wlan_ap_setup.py` auf den Pi und führe es mit root-Rechten aus

### Pi Pico

### Backend server

* Verbinde dich über ssh mit dem Backend
* Verbinde dich mit `nmtui` mit dem WiFi:
    1. Führe `nmtui` aus
    2. Wähle "Activate a connection"
    3. Wähle das Netzwerk aus und gebe das Passwort ein (Standard: Production, Production-01)
* Klone das Repository auf das Backend
* Installiere Docker Compose
* Zum Starten der Software führe jetzt `sudo docker compose up` im Projektverzeichnis aus

## Bedienung

Die Applikation lässt sich mit `sudo docker compose up/down` starten und beenden.  
Vor dem Start ist sicherzustellen, dass der WLAN-AP Pi hochgefahren und funktionstüchtig ist (z.B. indem geprüft wird,
ob das Backend ´mit dem zugehörigen WLAN verbunden ist).  
Der Pico wird durch Ausführen der `main.py` gestartet.
Nach dem Start kann eine Verbindung zum Netzwerk aufgebaut werden und
unter [https://local.kleber.data](https://local.kleber.data) das Web Dashboard besucht werden.  
Hier folgt eine Anmeldung mit [iotuser01]: [password] oder [admin]: [admin].
Danach wird das Dashboard angezeigt. 
Als Admin besteht außerdem die Möglichkeit alle Sensordaten als CSV-Datei zu exportieren. 

## Fazit



## Literatur und Hilfsmittel