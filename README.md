# Temperatur- und Luftfeuchtigkeitsregulierer

## Anforderungen

* 2 Raspberry Pi 4s
* 1 Pi Pico
* Ein Netzwerkkabel mit Internetzugriff
* 2 SD-Karten

## Installation

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