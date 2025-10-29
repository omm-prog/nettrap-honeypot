import socket
import threading
import json
import os
import sys
from src.logger import HoneypotLogger
from src.service_emulators import ServiceEmulator

class NetTrapHoneypot:
    def __init__(self, config_file="config/config.json"):
        self.load_config(config_file)
        self.logger = HoneypotLogger()
        self.service_emulator = ServiceEmulator(self.logger, self.config)
        self.sockets = []
        self.running = False
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            # Default config
            self.config = {
                "honeypot": {
                    "ports": [21, 22, 23, 80, 443],
                    "bind_address": "0.0.0.0",
                    "max_connections": 10
                }
            }
    
    def get_service_name(self, port):
        """Map port to service name"""
        service_map = {
            21: "FTP",
            22: "SSH", 
            23: "TELNET",
            80: "HTTP",
            443: "HTTPS",
            8080: "HTTP",
            2222: "SSH"
        }
        return service_map.get(port, f"PORT_{port}")
    
    def handle_client(self, client_socket, client_ip, port):
        """Handle individual client connection"""
        service_type = self.get_service_name(port)
        self.logger.log_connection(client_ip, port, service_type)
        
        try:
            if port in [22, 2222]:
                self.service_emulator.handle_ssh(client_socket, client_ip, port)
            elif port == 21:
                self.service_emulator.handle_ftp(client_socket, client_ip, port)
            elif port == 23:
                self.service_emulator.handle_telnet(client_socket, client_ip, port)
            elif port in [80, 443, 8080]:
                self.service_emulator.handle_http(client_socket, client_ip, port)
            else:
                # Generic handler for other ports
                self.service_emulator.handle_http(client_socket, client_ip, port)
                
        except Exception as e:
            self.logger.log_error(client_ip, port, f"Handler error: {e}")
        finally:
            client_socket.close()
    
    def start_port_listener(self, port):
        """Start listening on a specific port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            bind_addr = self.config['honeypot']['bind_address']
            sock.bind((bind_addr, port))
            sock.listen(self.config['honeypot']['max_connections'])
            
            self.sockets.append(sock)
            service_name = self.get_service_name(port)
            
            print(f"🎣 Honeypot listening on {service_name} port {port}")
            
            while self.running:
                try:
                    client_socket, client_addr = sock.accept()
                    client_ip = client_addr[0]
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_ip, port)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        self.logger.log_error("Unknown", port, f"Socket accept error: {e}")
                    break
                    
        except Exception as e:
            self.logger.log_error("Unknown", port, f"Port listener error: {e}")
    
    def start(self):
        """Start the honeypot"""
        print("🚀 Starting NetTrap Honeypot...")
        print("⚠️  Warning: Running honeypot may trigger security alerts!")
        print("📝 Logs will be saved in 'logs' directory")
        
        self.running = True
        
        # Start listener for each port
        threads = []
        for port in self.config['honeypot']['ports']:
            thread = threading.Thread(target=self.start_port_listener, args=(port,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        print("✅ All honeypot services are running!")
        print("🛑 Press Ctrl+C to stop the honeypot")
        
        try:
            # Keep main thread alive
            while self.running:
                for thread in threads:
                    if not thread.is_alive():
                        print("⚠️ A listener thread died, restarting...")
                        port = self.config['honeypot']['ports'][threads.index(thread)]
                        new_thread = threading.Thread(target=self.start_port_listener, args=(port,))
                        new_thread.daemon = True
                        new_thread.start()
                        threads[threads.index(thread)] = new_thread
                
                threading.Event().wait(5)
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the honeypot"""
        print("\n🛑 Stopping NetTrap Honeypot...")
        self.running = False
        
        for sock in self.sockets:
            try:
                sock.close()
            except:
                pass
        
        print("✅ Honeypot stopped successfully")

if __name__ == "__main__":
    honeypot = NetTrapHoneypot()
    honeypot.start()