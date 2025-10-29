import subprocess
import threading
import re
from datetime import datetime

class SimplePingMonitor:
    def __init__(self, logger, attack_map):
        self.logger = logger
        self.attack_map = attack_map
        self.running = False
        
    def monitor_ping_logs(self):
        """Monitor Windows ping logs using netstat and connection monitoring"""
        print("🔄 Ping monitor started - Monitoring network activity...")
        
        known_ips = set()
        
        while self.running:
            try:
                # Use netstat to detect incoming connections
                result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=10)
                
                # Parse netstat output for suspicious activity
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'ESTABLISHED' in line or 'SYN_RECEIVED' in line:
                        # Extract IP addresses
                        ip_match = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
                        for ip in ip_match:
                            if ip not in ['0.0.0.0', '127.0.0.1', '::1'] and ip not in known_ips:
                                known_ips.add(ip)
                                print(f"🔄 New network activity from: {ip}")
                                # Log as network scan
                                self.attack_map.add_network_scan(ip, "NETWORK_DISCOVERY", "New host detected")
                                
            except Exception as e:
                if self.running:
                    continue
            
            threading.Event().wait(5)  # Check every 5 seconds
    
    def start(self):
        self.running = True
        thread = threading.Thread(target=self.monitor_ping_logs, daemon=True)
        thread.start()
        
    def stop(self):
        self.running = False