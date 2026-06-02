# Temperature and Humidity Regulator

## Requirements

* 2 Raspberry Pi 4s
* 1 Pi Pico
* A
* 2 SD-Cards

## Installation

### WLAN AP

* Install the Raspberry Pi light Image on one of the Pis using the SD-Card. 
* Connect to the Pi using ssh or pi.connect.
* Place `wlan_ap_setup.py` from `/configurations` in your users root path. 
* Run that script using `sudo python3 wlan_ap_setup.py`.

### Pi Pico

### Backend server

* Install the Raspberry Pi light Image on one of the Pis using the SD-Card. 
* Connect to the Pi using ssh or pi.connect. 
* Clone the repository onto the Pi. 
* Install docker compose on the Pi.
* In the Project root directory run `sudo docker compose up`