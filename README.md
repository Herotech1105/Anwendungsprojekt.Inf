# Temperature and Humidity Regulator

## Requirements

* 2 Raspberry Pi 4s
* 1 Pi Pico
* Access to the internet using a network cable
* 2 SD-Cards

## Installation

### Pi Setup
* Install the Raspberry Pi light Image the Pis using the SD-Cards.
* Check one of the Pis for its MAC-address and note it for later use. This Pi will be the backend.

### WLAN AP
 
* Connect to the other Pi using ssh or pi.connect.
* Change the backend_mac_address in line 4 in `/conficuration/wlan_ap_setup.py` to the backends mac address. 
* Now copy the script to your users root directory on the WLAN Pi. 
* Run that script using `sudo python3 wlan_ap_setup.py`.

### Pi Pico

### Backend server

* Install the Raspberry Pi light Image on one of the Pis using the SD-Card. 
* Connect to the Pi using ssh or pi.connect. 
* Connect to the Wi-Fi using `nmtui`:
  1. Run `nmtui`
  2. Select "Activate a connection"
  3. Choose the Wi-Fi `Production` and enter the password `Production-01` 
* Clone the repository onto the Pi. 
* Install docker compose on the Pi.
* In the Project root directory run `sudo docker compose up`