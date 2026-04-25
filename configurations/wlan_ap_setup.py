import os
import subprocess


def write_file(path, content):
    """Writes to file and handles errors"""
    try:
        with open(path, 'w') as f:
            f.write(content)
    except OSError as e:
        print(f"Error writing to {path}: {e}")


def run_cmd(cmd):
    """Executes a shell command and handles errors"""
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {cmd}\n{e.stderr}")


def configure_ap():
    """Creates Configuration"""
    # 1. Configuration Parameters
    wlan_iface = "wlan0"
    eth_iface = "eth0"
    ssid = "Production"
    password = "Production-01"
    run_cmd("nmcli device set wlan0 managed no")

    print(f"--- Starting Configuration on {wlan_iface} ---")

    # 2. Stop services to prevent locks during config
    print("Stopping services")
    run_cmd("systemctl stop hostapd dnsmasq nftables")

    # 3. Hostapd Configuration
    print("Writing Hostapd-Configuration to '/etc/hostapd/hostapd.conf'")
    hostapd_conf = f"""
interface={wlan_iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel=7
wmm_enabled=1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
"""
    write_file("/etc/hostapd/hostapd.conf", hostapd_conf)

    # 4. Dnsmasq Configuration
    print("Writing DNSMASQ-Configuration to '/etc/dnsmasq.conf'")
    dnsmasq_conf = f"""
interface={wlan_iface}
bind-interfaces
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
domain=wlan
address=/gw.wlan/192.168.4.1
"""
    write_file("/etc/dnsmasq.conf", dnsmasq_conf)

    # 5. Interface Setup
    print(f"Setting static IP 192.168.4.1 on {wlan_iface}...")
    run_cmd(f"ip link set {wlan_iface} down")
    run_cmd(f"ip addr flush dev {wlan_iface}")
    run_cmd(f"ip addr add 192.168.4.1/24 dev {wlan_iface}")
    run_cmd(f"ip link set {wlan_iface} up")

    # 6. Enable IP Forwarding (Persistent)
    print("Enable persistent IP Forwarding")
    run_cmd("sysctl -w net.ipv4.ip_forward=1")
    ip_sysctl = "net.ipv4.ip_forward=1"
    write_file("/etc/sysctl.conf", ip_sysctl)

    # 7. Firewall & NAT
    print("Configuring NAT")
    nat_config = """#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0;
        policy drop;
        iif "lo" accept
        ct state established,related accept
        tcp dport 22 accept 
        ip protocol icmp accept
        iif "wlan0" udp dport { 53, 67 } accept
    }

    chain output {
        type filter hook output priority 0;
        policy accept; # Explicitly allow you to send data out
    }
    
    chain forward {
        type filter hook forward priority 0; policy accept;
    }
}

table ip nat {
    chain prerouting {
        type nat hook prerouting priority dstnat;
        policy accept;
    }
    chain postrouting {
        type nat hook postrouting priority srcnat;
        policy accept;
        oif "eth0" masquerade
    }
}
"""

    write_file("/etc/nftables.conf", nat_config)

    # 8. Start Services
    print("Restarting services...")
    run_cmd("systemctl unmask hostapd")
    run_cmd("systemctl enable hostapd dnsmasq nftables")
    run_cmd("systemctl start hostapd dnsmasq nftables")

    # 9. Setup Complete
    print(f"\n--- Setup Complete! ---")
    print(f"SSID: {ssid}")
    print(f"Gateway: 192.168.4.1")


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Please run this script with 'sudo'.")
    else:
        configure_ap()

# Sources:
# https://www.elektronik-kompendium.de/sites/raspberry-pi/2002171.htm 23.04.2026
# API Kapitel 2 Folien
# https://raspberrypi-guide.github.io/networking/create-wireless-access-point 23.04.2026
# https://u-labs.de/portal/einstiegt-in-nftables-so-funktioniert-die-neue-firewall-unterschiede-zu-iptables/ 24.04.2026
