from flask import Flask, render_template, jsonify
import subprocess
import platform

app = Flask(__name__)

def scan_wifi_networks():
    """
    Scans for Wi-Fi networks based on the operating system.
    Returns a list of networks with SSID, signal strength, and security.
    """
    wifi_networks = []

    try:
        if platform.system() == "Windows":
            # Windows command to list networks
            output = subprocess.check_output("netsh wlan show networks mode=bssid", shell=True).decode("utf-8", errors="ignore")
            networks = output.split("\n")
            current_network = {}
            for line in networks:
                if "SSID" in line:
                    if current_network:
                        wifi_networks.append(current_network)
                        current_network = {}
                    current_network["SSID"] = line.split(":")[1].strip()
                elif "Signal" in line:
                    current_network["Signal"] = line.split(":")[1].strip()
                elif "Authentication" in line:
                    current_network["Security"] = line.split(":")[1].strip()
            if current_network:
                wifi_networks.append(current_network)

        elif platform.system() == "Linux" or platform.system() == "Darwin":
            # Linux/macOS command to list networks
            output = subprocess.check_output("nmcli -t -f SSID,SIGNAL,SECURITY dev wifi", shell=True).decode("utf-8", errors="ignore")
            networks = output.split("\n")
            for network in networks:
                if network:
                    ssid, signal, security = network.split(":")
                    wifi_networks.append({"SSID": ssid, "Signal": signal, "Security": security})

    except Exception as e:
        print("Error scanning networks:", e)
    
    return wifi_networks

@app.route('/')
def index():
    """
    Renders the main index.html page.
    """
    return render_template('index.html')

@app.route('/scan', methods=['GET'])
def scan():
    """
    Returns JSON data of scanned Wi-Fi networks.
    """
    networks = scan_wifi_networks()
    return jsonify(networks)

if __name__ == "__main__":
    app.run(debug=True)
