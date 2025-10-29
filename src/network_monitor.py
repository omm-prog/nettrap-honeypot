import socket
import struct
import threading
import time
from datetime import datetime
import os
import subprocess
from src.logger import HoneypotLogger

class NetworkMonitor:
    def __init__(self, logger, attack_map):
        self.logger = logger
        self.attack_map = attack_map
        self.running = False
        self.icmp_socket = None
        
    def start_icmp_monitor(self):
        """Monitor ICMP (ping) requests"""
        try:
            # Create raw socket to capture ICMP packets
            self.icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            self.icmp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**30)
            
            print("🎯 ICMP/Ping Monitor Started - Listening for ping requests...")
            
            while self.running:
                try:
                    packet, address = self.icmp_socket.recvfrom(1024)
                    ip_header = packet[0:20]
                    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
                    
                    version_ihl = iph[0]
                    ihl = version_ihl & 0xF
                    iph_length = ihl * 4
                    
                    src_ip = socket.inet_ntoa(iph[8])
                    
                    # Log the ping request
                    self.logger.log_connection(src_ip, "ICMP", "PING")
                    if self.attack_map:
                        self.attack_map.add_attack(src_ip, "ICMP", "PING", "ICMP Echo Request")
                        
                    print(f"🔄 Ping detected from {src_ip}")
                    
                except socket.error as e:
                    if self.running:
                        continue
                    break
                    
        except Exception as e:
            print(f"❌ ICMP Monitor Error: {e}")
            print("💡 Note: Raw socket requires Administrator privileges on Windows")
    
    def start_port_scan_detector(self):
        """Detect port scanning attempts"""
        print("🔍 Port Scan Detector Started...")
        # This would monitor for rapid connection attempts across multiple ports
        # For now, we'll rely on the individual port listeners
    
    def start_arp_monitor(self):
        """Monitor ARP requests for network reconnaissance"""
        try:
            print("🌐 ARP Monitor Started - Watching for network discovery...")
            # Windows ARP monitoring would require WinPcap or similar
            # For now, we'll implement a simple version
        except Exception as e:
            print(f"❌ ARP Monitor not available: {e}")
    
    def start_all_monitors(self):
        """Start all network monitoring services"""
        self.running = True
        
        # Start ICMP monitor in separate thread
        icmp_thread = threading.Thread(target=self.start_icmp_monitor, daemon=True)
        icmp_thread.start()
        
        # Start other monitors
        self.start_port_scan_detector()
        self.start_arp_monitor()
        
        print("✅ All network monitors started!")
    
    def stop(self):
        """Stop all monitors"""
        self.running = False
        if self.icmp_socket:
            self.icmp_socket.close()