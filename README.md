# 🕸️ NetTrap Honeypot

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

*A lightweight, modular network honeypot for detecting and analyzing suspicious network activities*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-project-structure) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

**NetTrap Honeypot** is a sophisticated yet lightweight network security tool designed to detect, simulate, and log malicious activities on your network. Built with modularity and ease-of-use in mind, it provides comprehensive network monitoring and service emulation capabilities for security research and defensive operations.

### Why NetTrap?

- 🎯 **Trap Attackers**: Simulate vulnerable services to attract and study attack patterns
- 📊 **Real-time Monitoring**: Track network connections and identify suspicious activities
- 📝 **Detailed Logging**: Comprehensive event logging for forensic analysis
- 🔧 **Easy to Use**: Simple setup with automated batch scripts
- 🧩 **Modular Design**: Extensible architecture for custom implementations

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Network Monitoring** | Real-time tracking of network connections using Windows netstat |
| **Service Emulation** | Simulates popular network services (SSH, FTP, HTTP, etc.) to attract attackers |
| **Attack Detection** | Identifies port scanning, brute force attempts, and suspicious connection patterns |
| **Event Logging** | Structured logging system for all detected events and attacks |
| **Attack Mapping** | Visual representation of attack sources and patterns |
| **Dashboard Interface** | Web-based dashboard for monitoring honeypot activity |

### Technical Highlights

- ⚡ Lightweight and resource-efficient
- 🐍 Pure Python implementation
- 🔌 Modular plugin architecture
- 📦 Easy dependency management
- 🖥️ Windows-optimized (with cross-platform potential)

---

## 🚀 Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+** ([Download](https://www.python.org/downloads/))
- **Windows OS** (required for netstat-based monitoring)
- **pip** (Python package manager)
- **Git** ([Download](https://git-scm.com/downloads))

### Quick Setup

1. **Clone the repository**

```bash
git clone https://github.com/omm-prog/nettrap-honeypot.git
cd nettrap-honeypot
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run setup script**

```bash
setup.bat
```

That's it! You're ready to start trapping attacks. 🎉

---

## 💻 Usage

### Starting the Honeypot

#### Method 1: Using Batch Script (Recommended)

```bash
start_honeypot.bat
```

#### Method 2: Manual Execution

```bash
python src/honeypot.py
```

### Running the Dashboard

Monitor your honeypot activity through the web dashboard:

```bash
start_dashboard.bat
```

Then open your browser and navigate to: `http://localhost:8080`

### Network Monitoring Only

To run only the network monitoring component:

```bash
python src/ping_monitor.py
```

### Command Line Options

```bash
# Start with custom port
python src/honeypot.py --port 8080

# Enable verbose logging
python src/honeypot.py --verbose

# Specify services to emulate
python src/honeypot.py --services ssh,ftp,http
```

---

## 📁 Project Structure

```
nettrap-honeypot/
│
├── 📂 src/
│   ├── 🐝 honeypot.py              # Main honeypot orchestrator
│   ├── 📡 ping_monitor.py          # Network activity monitor
│   ├── 🎭 service_emulators.py     # Service emulation engine
│   ├── 🗺️ attack_map.py            # Attack visualization and mapping
│   ├── 📊 network_monitor.py       # Network monitoring utilities
│   ├── 📝 logger.py                # Logging system
│   └── 🎨 dashboard.py             # Web dashboard interface
│
├── 📂 logs/                         # Event and attack logs
├── 📂 config/                       # Configuration files
│
├── ⚙️ setup.bat                     # Setup automation script
├── 🚀 start_honeypot.bat           # Honeypot launcher
├── 📊 start_dashboard.bat          # Dashboard launcher
├── 📋 requirements.txt             # Python dependencies
├── 📖 README.md                    # Documentation (you are here)
└── 📄 LICENSE                      # License information

```

---

## 🔧 Configuration

### Basic Configuration

Edit the `config/honeypot.conf` file to customize your honeypot:

```ini
[honeypot]
listen_address = 0.0.0.0
port_range = 20-9999
log_level = INFO

[services]
enable_ssh = true
enable_ftp = true
enable_http = true
enable_telnet = true

[monitoring]
scan_interval = 5
alert_threshold = 10
```

### Advanced Options

For advanced configuration options, see the [Configuration Guide](docs/configuration.md).

---

## 📊 Module Overview

### Core Modules

#### 🐝 `honeypot.py`
Main orchestration engine that coordinates all components and manages the event loop.

#### 📡 `ping_monitor.py`
Monitors network activity using Windows netstat, detecting new connections and potential port scans.

#### 🎭 `service_emulators.py`
Simulates vulnerable network services to attract and log malicious connection attempts.

#### 🗺️ `attack_map.py`
Provides attack visualization and geographic mapping of attack sources.

#### 📊 `network_monitor.py`
Low-level network monitoring utilities for packet analysis and connection tracking.

#### 📝 `logger.py`
Centralized logging system with support for multiple output formats and log rotation.

---

## 📈 Logs and Reports

### Log Files

Logs are stored in the `logs/` directory:

- `honeypot.log` - Main honeypot events
- `attacks.log` - Detected attack attempts
- `connections.log` - All network connections
- `services.log` - Service emulation events

### Viewing Logs

```bash
# View live logs
tail -f logs/honeypot.log

# Search for specific IP
grep "192.168.1.100" logs/attacks.log
```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push** to your branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guidelines for Python code
- Add tests for new features
- Update documentation as needed
- Write clear commit messages

---

## 🛡️ Security & Disclaimer

### ⚠️ Important Notice

This tool is designed for **educational and research purposes only**. 

- ✅ Use only on networks you own or have explicit permission to test
- ✅ Follow all applicable laws and regulations
- ✅ Do not use for malicious purposes
- ❌ The authors are not responsible for misuse or damage

### Best Practices

1. Run the honeypot in an isolated environment
2. Regularly review and analyze logs
3. Keep the software updated
4. Follow responsible disclosure practices
5. Document all testing activities

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Developed and maintained by [omm-prog](https://github.com/omm-prog)**

### Connect

- 🐙 GitHub: [@omm-prog](https://github.com/omm-prog)
- 📧 Email: [Contact](mailto:omchauhan2026@gmail.com)

---

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project
- Inspired by the network security and honeypot community
- Built with ❤️ using Python

---

## 📚 Additional Resources

- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [API Documentation](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star!**

[![GitHub stars](https://img.shields.io/github/stars/omm-prog/nettrap-honeypot?style=social)](https://github.com/omm-prog/nettrap-honeypot)

Made with 🕸️ by security enthusiasts, for security enthusiasts

</div>
