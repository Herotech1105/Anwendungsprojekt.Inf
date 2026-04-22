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

    print(f"--- Starting Configuration on {wlan_iface} ---")

    # 2. Stop services to prevent locks during config
    print("Stopping hostapd and dnsmasq")
    run_cmd("systemctl stop hostapd dnsmasq")

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

    # 7. Firewall & NAT (Flush old rules to prevent duplicates)
    print("Configuring NAT and Routing...")
    run_cmd("iptables -F")
    run_cmd("iptables -t nat -F")
    run_cmd(f"iptables -t nat -A POSTROUTING -o {eth_iface} -j MASQUERADE")
    run_cmd(f"iptables -A FORWARD -i {eth_iface} -o {wlan_iface} -m state --state RELATED,ESTABLISHED -j ACCEPT")
    run_cmd(f"iptables -A FORWARD -i {wlan_iface} -o {eth_iface} -j ACCEPT")

    # 8. Start Services
    print("Restarting services...")
    run_cmd("systemctl unmask hostapd")
    run_cmd("systemctl enable hostapd dnsmasq")
    run_cmd("systemctl start hostapd dnsmasq")

    # 9. Setup Complete
    print(f"\n--- Setup Complete! ---")
    print(f"SSID: {ssid}")
    print(f"Gateway: 192.168.4.1")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Please run this script with 'sudo'.")
    else:
        configure_ap()
