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

Datum:  
Problemstellung:  
Verantwortlicher:  
GANT-Diagramm:

| Datei | Änderung | Erklärung |
|-------|----------|-----------|

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

