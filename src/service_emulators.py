import socket
import time
import random
from datetime import datetime

class ServiceEmulator:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
    
    def handle_ssh(self, client_socket, client_ip, port):
        """Emulate SSH service"""
        try:
            banner = self.config['services']['ssh']['banner']
            prompt = self.config['services']['ssh']['prompt']
            
            client_socket.send(f"{banner}\r\n".encode())
            time.sleep(self.config['honeypot']['banner_delay'])
            
            client_socket.send(prompt.encode())
            
            while True:
                data = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
                if not data:
                    break
                
                self.logger.log_command(client_ip, port, "SSH", data)
                
                # Fake responses
                if "ssh" in data.lower() or "login" in data.lower():
                    client_socket.send(b"Password: ")
                elif data:
                    client_socket.send(b"Access denied\r\n")
                    break
                    
        except Exception as e:
            self.logger.log_error(client_ip, port, f"SSH error: {e}")
        finally:
            client_socket.close()
    
    def handle_ftp(self, client_socket, client_ip, port):
        """Emulate FTP service"""
        try:
            banner = self.config['services']['ftp']['banner']
            prompt = self.config['services']['ftp']['prompt']
            
            client_socket.send(f"{banner}\r\n".encode())
            
            while True:
                data = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
                if not data:
                    break
                
                self.logger.log_command(client_ip, port, "FTP", data)
                
                # Fake FTP responses
                if "USER" in data.upper():
                    client_socket.send(b"331 Password required\r\n")
                elif "PASS" in data.upper():
                    client_socket.send(b"530 Login incorrect\r\n")
                elif "QUIT" in data.upper():
                    client_socket.send(b"221 Goodbye\r\n")
                    break
                else:
                    client_socket.send(b"500 Unknown command\r\n")
                    
        except Exception as e:
            self.logger.log_error(client_ip, port, f"FTP error: {e}")
        finally:
            client_socket.close()
    
    def handle_telnet(self, client_socket, client_ip, port):
        """Emulate Telnet service"""
        try:
            banner = self.config['services']['telnet']['banner']
            prompt = self.config['services']['telnet']['prompt']
            
            client_socket.send(f"{banner}\r\n".encode())
            time.sleep(1)
            client_socket.send(prompt.encode())
            
            while True:
                data = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
                if not data:
                    break
                
                self.logger.log_command(client_ip, port, "TELNET", data)
                
                # Fake login responses
                if data:
                    client_socket.send(b"Password: ")
                    password_data = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
                    if password_data:
                        self.logger.log_command(client_ip, port, "TELNET", f"Password: {password_data}")
                    client_socket.send(b"Login incorrect\r\n")
                    break
                    
        except Exception as e:
            self.logger.log_error(client_ip, port, f"Telnet error: {e}")
        finally:
            client_socket.close()
    
    def handle_http(self, client_socket, client_ip, port):
        """Emulate HTTP service"""
        try:
            data = client_socket.recv(4096).decode('utf-8', errors='ignore')
            
            if data:
                self.logger.log_command(client_ip, port, "HTTP", data.split('\r\n')[0] if '\r\n' in data else data)
                
                # Send fake HTTP response
                response = """HTTP/1.1 200 OK
Server: Apache/2.4.41 (Win64)
Content-Type: text/html
Connection: close

<html>
<head><title>Test Page</title></head>
<body>
<h1>Welcome</h1>
<p>Site under construction</p>
</body>
</html>"""
                
                client_socket.send(response.replace('\n', '\r\n').encode())
                
        except Exception as e:
            self.logger.log_error(client_ip, port, f"HTTP error: {e}")
        finally:
            client_socket.close()