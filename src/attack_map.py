import json
import threading
import time
from datetime import datetime
from flask import Flask, render_template_string, jsonify
import requests
import socket

class RealTimeAttackMap:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.attacks = []
        self.app = Flask(__name__)
        self.setup_routes()
        
    def setup_routes(self):
        """Setup Flask routes"""
        @self.app.route('/')
        def index():
            return self.render_attack_map()
        
        @self.app.route('/api/attacks')
        def get_attacks():
            return jsonify(self.attacks)
        
        @self.app.route('/api/stats')
        def get_stats():
            stats = {
                'total_attacks': len(self.attacks),
                'unique_attackers': len(set(attack['ip'] for attack in self.attacks)),
                'ports_targeted': list(set(attack['port'] for attack in self.attacks)),
                'latest_attack': self.attacks[-1] if self.attacks else None
            }
            return jsonify(stats)
    
    def get_ip_location(self, ip_address):
        """Get geographic location for IP address using ip-api.com"""
        try:
            # Skip local IPs
            if ip_address in ['127.0.0.1', 'localhost']:
                return 0, 0, "Localhost", "🌐 Local"
            
            if ip_address.startswith('192.168.') or ip_address.startswith('10.') or ip_address.startswith('172.'):
                return 0, 0, "Local Network", "🏠 Internal"
            
            # Use free IP geolocation service (no API key needed)
            response = requests.get(f'http://ip-api.com/json/{ip_address}?fields=status,message,country,city,lat,lon,isp', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    lat = data.get('lat', 0)
                    lon = data.get('lon', 0)
                    city = data.get('city', 'Unknown City')
                    country = data.get('country', 'Unknown Country')
                    return lat, lon, f"{city}, {country}", "🌍 Remote"
            
            return 0, 0, "Unknown Location", "❓ Unknown"
        except Exception as e:
            print(f"Geolocation error for {ip_address}: {e}")
            return 0, 0, "Geolocation Failed", "🚫 Error"
    
    def add_attack(self, ip_address, port, service_type, command=None):
        """Add new attack to the map"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get location data
        lat, lon, location, location_type = self.get_ip_location(ip_address)
        
        attack_data = {
            'ip': ip_address,
            'port': port,
            'service': service_type,
            'timestamp': timestamp,
            'location': location,
            'location_type': location_type,
            'lat': lat,
            'lon': lon,
            'command': command[:100] + '...' if command and len(command) > 100 else command
        }
        
        self.attacks.append(attack_data)
        
        # Keep only last 500 attacks to prevent memory issues
        if len(self.attacks) > 500:
            self.attacks = self.attacks[-500:]
        
        print(f"🗺️  Attack mapped: {ip_address} -> {service_type}:{port}")
        return attack_data

    def add_network_scan(self, ip_address, scan_type, details=None):
        """Add network scanning activity to the map"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get location data
        lat, lon, location, location_type = self.get_ip_location(ip_address)
        
        scan_data = {
            'ip': ip_address,
            'port': scan_type,
            'service': 'NETWORK_SCAN',
            'timestamp': timestamp,
            'location': location,
            'location_type': location_type,
            'lat': lat,
            'lon': lon,
            'command': details or f"{scan_type} activity detected"
        }
        
        self.attacks.append(scan_data)
        
        # Keep only last 500 attacks to prevent memory issues
        if len(self.attacks) > 500:
            self.attacks = self.attacks[-500:]
        
        print(f"🕵️  Network Scan: {ip_address} - {scan_type} - {details}")
        return scan_data
    
    def generate_map_html(self):
        """Generate simple map visualization using HTML5"""
        # Create attack visualization
        attacks_html = ""
        for attack in self.attacks[-20:]:  # Show last 20 attacks
            attacks_html += f"""
            <div class="attack-item">
                <span class="service-badge {attack['service'].lower()}">{attack['service']}</span>
                <span class="ip-address">{attack['ip']}</span>
                <span class="location">{attack['location']}</span>
                <span class="time">{attack['timestamp']}</span>
            </div>
            """
        
        return attacks_html
    
    def get_service_distribution(self):
        """Get count of attacks per service"""
        distribution = {}
        for attack in self.attacks:
            service = attack['service']
            distribution[service] = distribution.get(service, 0) + 1
        return distribution
    
    def render_attack_map(self):
        """Render the attack map HTML"""
        attacks_html = self.generate_map_html()
        service_distribution = self.get_service_distribution()
        
        # Create service distribution HTML
        service_html = ""
        for service, count in service_distribution.items():
            service_html += f'<div class="stat-item"><span>{service}:</span><span class="stat-value">{count}</span></div>'
        
        html_template = f'''
<!DOCTYPE html>
<html>
<head>
    <title>NetTrap - Real-Time Attack Map</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ 
            margin: 0; 
            padding: 0; 
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .dashboard {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .stats-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .stats-card h3 {{
            margin-top: 0;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .stat-item {{
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 5px;
        }}
        
        .stat-value {{
            font-weight: bold;
            color: #667eea;
        }}
        
        .attacks-list {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            grid-column: 1 / -1;
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .attack-item {{
            display: grid;
            grid-template-columns: 80px 150px 1fr 200px;
            gap: 15px;
            padding: 12px;
            border-bottom: 1px solid #eee;
            align-items: center;
        }}
        
        .attack-item:hover {{
            background: #f8f9fa;
        }}
        
        .service-badge {{
            padding: 4px 8px;
            border-radius: 4px;
            color: white;
            font-size: 0.8em;
            font-weight: bold;
            text-align: center;
        }}
        
        .ssh {{ background: #dc3545; }}
        .ftp {{ background: #007bff; }}
        .http {{ background: #28a745; }}
        .telnet {{ background: #ffc107; color: black; }}
        .https {{ background: #6f42c1; }}
        .network_scan {{ background: #000000; }}
        
        .ip-address {{
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }}
        
        .location {{
            color: #666;
        }}
        
        .time {{
            font-size: 0.9em;
            color: #999;
        }}
        
        .controls {{
            text-align: center;
            margin: 20px 0;
        }}
        
        .btn {{
            background: white;
            color: #667eea;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            margin: 0 5px;
            transition: all 0.3s;
        }}
        
        .btn:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }}
        
        @media (max-width: 768px) {{
            .dashboard {{
                grid-template-columns: 1fr;
            }}
            
            .attack-item {{
                grid-template-columns: 1fr;
                gap: 5px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 NetTrap Attack Dashboard</h1>
            <div class="subtitle">Real-time honeypot attack monitoring</div>
        </div>
        
        <div class="dashboard">
            <div class="stats-card">
                <h3>📊 Attack Statistics</h3>
                <div class="stat-item">
                    <span>Total Attacks:</span>
                    <span class="stat-value" id="totalAttacks">{len(self.attacks)}</span>
                </div>
                <div class="stat-item">
                    <span>Unique Attackers:</span>
                    <span class="stat-value" id="uniqueAttackers">{len(set(attack['ip'] for attack in self.attacks))}</span>
                </div>
                <div class="stat-item">
                    <span>Services Targeted:</span>
                    <span class="stat-value" id="servicesTargeted">{len(set(attack['service'] for attack in self.attacks))}</span>
                </div>
                <div class="stat-item">
                    <span>Latest Attack:</span>
                    <span class="stat-value" id="latestAttack">{self.attacks[-1]['timestamp'] if self.attacks else 'None'}</span>
                </div>
            </div>
            
            <div class="stats-card">
                <h3>🎯 Service Distribution</h3>
                <div id="serviceDistribution">
                    {service_html if service_html else '<div class="stat-item"><span>No attacks yet</span><span class="stat-value">0</span></div>'}
                </div>
            </div>
            
            <div class="attacks-list">
                <h3>🔍 Recent Attacks (Last 20)</h3>
                <div class="attack-list-header attack-item">
                    <div><strong>Service</strong></div>
                    <div><strong>IP Address</strong></div>
                    <div><strong>Location</strong></div>
                    <div><strong>Time</strong></div>
                </div>
                {attacks_html if attacks_html else '<div style="text-align: center; padding: 40px; color: #666;">No attacks recorded yet. Wait for connections...</div>'}
            </div>
        </div>
        
        <div class="controls">
            <button class="btn" onclick="refreshStats()">🔄 Refresh Stats</button>
            <button class="btn" onclick="location.reload()">🔄 Refresh Page</button>
            <button class="btn" onclick="clearAttacks()">🗑️ Clear History</button>
        </div>
    </div>

    <script>
        function refreshStats() {{
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('totalAttacks').textContent = data.total_attacks;
                    document.getElementById('uniqueAttackers').textContent = data.unique_attackers;
                    document.getElementById('servicesTargeted').textContent = data.ports_targeted.length;
                    if (data.latest_attack) {{
                        document.getElementById('latestAttack').textContent = data.latest_attack.timestamp;
                    }}
                }});
        }}

        function clearAttacks() {{
            if (confirm('Are you sure you want to clear all attack history?')) {{
                // This would need a backend endpoint to clear attacks
                alert('Clear functionality would be implemented with a backend endpoint');
            }}
        }}

        // Auto-refresh stats every 5 seconds
        setInterval(refreshStats, 5000);
        
        // Load stats on page load
        refreshStats();
    </script>
</body>
</html>
'''
        return html_template
    
    def start_dashboard(self):
        """Start the Flask dashboard"""
        print(f"🗺️  Starting Attack Dashboard on http://{self.host}:{self.port}")
        print("📍 Open your web browser to view the real-time attack map!")
        try:
            self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
        except Exception as e:
            print(f"❌ Failed to start dashboard: {e}")
            print("💡 Try changing the port by modifying 'port=5000' in attack_map.py")

def start_attack_map_daemon():
    """Start attack map in a separate thread"""
    try:
        attack_map = RealTimeAttackMap()
        thread = threading.Thread(target=attack_map.start_dashboard, daemon=True)
        thread.start()
        print("✅ Attack dashboard started successfully!")
        return attack_map
    except Exception as e:
        print(f"❌ Failed to start attack dashboard: {e}")
        return None