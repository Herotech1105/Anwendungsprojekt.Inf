# Temperatur- und Luftfeuchtigkeitsregulierer

## Anforderungen

* 2 Raspberry Pi 4 B
* 1 Raspberry Pi Pico WH
* Ein Netzwerkkabel mit Internetzugriff
* 2 Micro-SD-Karten
* Netzteile für beide Raspberry Pi 4 B und Aktoren
* Lüfter und Heizung mit passender Leistung
* USB-Kabel mit Micro-USB auf USB-A oder USB-C
* Thonny Software

* Optional für dieses Projekt:
    - Peltier-Element für aktive Kühlung
    - 3D-Druck-Gehäuse
    - Wasserbox für Luftfeuchtigkeit
    - LCD-Display für visuelle Anzeige

## Installation

### Pi Setup

* Installiere das Raspberry Pi OS light Image auf beiden Micro-SDs für die Pis
* Lies die MAC-Addresse eines Pis aus; dieser Pi wird später zum Backend

### WLAN AP

* Verbinde den WLAN Pi über ein Netzwerkkabel mit dem Internet
* Stelle eine Verbindung zum Pi via ssh her
* Setze backend_mac_address in Zeile 4 in `/conficuration/wlan_ap_setup.py` auf die MAC-Addresse des Backends
* Führe `sudo apt install hostapd dnsmasq` auf dem Pi aus
* Kopiere jetzt das Skript `wlan_ap_setup.py` auf den Pi und führe es mit root-Rechten aus

### Pi Pico

* Verbinde den Pi Pico über Micro-USB an USB-A/USB-C eines Endgerätes mit Thonny:
    1. BOOTSEL-Taste (weiße Taste auf Pico) gedrückt halten
    2. An Entwicklungs-Endgerät per USB-Kabel anschließen
    3. .uf2-Datei mit der MicroPython-Firmware auf das Laufwerk "RPI-RP2" per Drag und Drop kopieren.
    4. Pico startet neu
* Danach kann der Pi Pico immer wieder eingesteckt und Thonny geöffnet werden
* Der Pi Pico verbindet sich dann automatisch mit Thonny
* main.py auswählen und "Run current script" Button klicken um zu starten
* Bei Spannungsversorgung ohne Datenfluss (zum Beispiel Pico direkt über USB-Kabel an Netzteil) startet main.py
  automatisch

### Backend server

* Verbinde dich über ssh mit dem Backend
* Verbinde dich mit `nmtui` mit dem WiFi:
    1. Führe `nmtui` aus
    2. Wähle "Activate a connection"
    3. Wähle das Netzwerk aus und gebe das Passwort ein (Standard: Production, Production-01)
* Klone das Repository auf das Backend
* Installiere Docker Compose
* Zum Starten der Software führe jetzt `sudo docker compose up` im Projektverzeichnis aus