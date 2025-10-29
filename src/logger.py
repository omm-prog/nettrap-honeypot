import logging
import json
import os
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for Windows
init()

class HoneypotLogger:
    def __init__(self, log_dir="logs", attack_map=None):
        self.log_dir = log_dir
        self.attack_map = attack_map  # NEW: Attack map integration
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging directory and files"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Main log file
        log_file = os.path.join(self.log_dir, f"honeypot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('nettrap')
    
    def log_connection(self, client_ip, port, service_type):
        """Log new connection attempts"""
        message = f"CONNECTION - {client_ip} connected to {service_type} on port {port}"
        self.logger.info(Fore.GREEN + message + Style.RESET_ALL)
        
        # NEW: Add to attack map
        if self.attack_map:
            self.attack_map.add_attack(client_ip, port, service_type)
        
        # Also log to connections file
        self.log_to_json({
            "timestamp": datetime.now().isoformat(),
            "event_type": "connection",
            "client_ip": client_ip,
            "port": port,
            "service_type": service_type
        })
    
    def log_command(self, client_ip, port, service_type, command):
        """Log commands/data received"""
        message = f"COMMAND - {client_ip} on {service_type}:{port} - {command}"
        self.logger.warning(Fore.YELLOW + message + Style.RESET_ALL)
        
        # NEW: Update attack map with command data
        if self.attack_map:
            self.attack_map.add_attack(client_ip, port, service_type, command)
        
        # Also log to commands file
        self.log_to_json({
            "timestamp": datetime.now().isoformat(),
            "event_type": "command",
            "client_ip": client_ip,
            "port": port,
            "service_type": service_type,
            "command": command
        }, "commands")
    
    def log_error(self, client_ip, port, error_message):
        """Log errors"""
        message = f"ERROR - {client_ip} on port {port} - {error_message}"
        self.logger.error(Fore.RED + message + Style.RESET_ALL)
    
    def log_to_json(self, data, log_type="connections"):
        """Log structured data to JSON file"""
        json_file = os.path.join(self.log_dir, f"{log_type}.json")
        
        try:
            existing_data = []
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = []
            
            existing_data.append(data)
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to write JSON log: {e}")