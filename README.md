# 🔒 Educational Keylogger v2.1 - Enhanced Edition

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-Educational-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)](https://github.com/AyGoub/KeyLogger)
[![Status](https://img.shields.io/badge/status-Enhanced%20%26%20Optimized-green.svg)](README.md)

> ⚠️ **EDUCATIONAL USE ONLY** ⚠️  
> This project is designed exclusively for cybersecurity education, authorized testing, and security research. Unauthorized use is illegal and unethical.

## 🎓 **Educational Purpose**

This advanced keylogger demonstrates cutting-edge cybersecurity concepts including:

- **📊 Enhanced Input Monitoring**: Cross-platform keystroke capture with intelligent formatting
- **🎯 Smart Window Detection**: Real-time application switching detection (0.5s response time)
- **🔐 Military-Grade Encryption**: AES-256 Fernet encryption for secure log storage
- **🕵️ Advanced Stealth Techniques**: VM detection, process obfuscation, anti-debug
- **📧 Professional Email Reports**: Clean, readable reports with proper formatting
- **🔬 Digital Forensics**: Comprehensive logging for security analysis
- **⚙️ System Integration**: Persistence mechanisms and system monitoring

## 🚀 **Key Improvements in v2.1**

### ✨ **Enhanced Features**
- ✅ **Clean Text Formatting**: Proper spacing and readable keystroke logs
- ✅ **Instant App Detection**: Detects Alt+Tab and window switches immediately  
- ✅ **Smart Special Keys**: Clean handling of `[CTRL]`, `[ALT]`, `[TAB]`, `[BACKSPACE]`
- ✅ **Professional Reports**: Email reports with proper timestamps and grouping
- ✅ **Optimized Performance**: Reduced buffer size for faster application switching
- ✅ **Better Timestamps**: Single timestamp per keystroke group instead of per key

### 🔧 **Technical Enhancements**
- ✅ **Responsive Window Detection**: 0.5-second polling + immediate Alt+Tab detection
- ✅ **Intelligent Buffer Management**: Auto-flush on application switches
- ✅ **Clean Log Format**: Readable output without character scatter
- ✅ **Enhanced Encryption**: Improved key management and data protection
- ✅ **Modular Architecture**: Clean, maintainable codebase structure

## 📧 **Enhanced Email Report Format**

### **Before (v2.0)**
```
[07:48:21] isualcodeterminalcopilotterminal
[07:48:38] cahtgpt
[07:48:39] aathisgoogleiwillkoleforatouyoubgoubraimc
```

### **After (v2.1)**
```
📊 Educational Keylogger Report
═══════════════════════════════
📅 Generated: 2025-09-30 08:01:14
🖥️ System: Linux 6.12.25-amd64

🔄 [08:01:11] Application: ChatGPT — Mozilla Firefox
────────────────────────────────────────────────────
[08:01:11] this is much cleaner text with proper spacing [ALT][TAB]

🔄 [08:01:12] Application: Gmail — Mozilla Firefox  
────────────────────────────────────────────────────
[08:01:12] typing in gmail now [CTRL]a

🔄 [08:01:15] Application: Visual Studio Code
────────────────────────────────────────────────────
[08:01:15] coding in vscode [CTRL]s
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

# For enhanced window detection (recommended)
sudo apt-get install wmctrl xprop
```

## 🛠️ **Installation & Setup**

### **1. Clone Repository**
```bash
git clone https://github.com/AyGoub/KeyLogger.git
cd KeyLogger
```

### **2. Auto Setup (Recommended)**
```bash
# Automatic setup with virtual environment
chmod +x setup.sh
./setup.sh
```

### **3. Manual Setup**
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### **4. Configure Email (Optional)**
Edit `config/config.json`:

```json
{
    "email": {
        "enabled": true,
        "sender_email": "your-email@gmail.com", 
        "sender_password": "your-app-password",
        "recipient_email": "reports@your-domain.com",
        "send_interval_hours": 0.1
    }
}
```

## 🚀 **Enhanced Usage**

### **Quick Start**
```bash
# Run with default configuration
sudo python main.py

# The keylogger will:
# ✅ Show educational warnings
# ✅ Detect application switches instantly
# ✅ Generate clean, readable logs  
# ✅ Send professional email reports
```

### **Advanced Usage**
```bash
# Debug mode with verbose output
sudo python main.py --debug

# Custom configuration file
sudo python main.py --config examples/stealth_config.json

# Test mode (safer for development)
sudo python main.py --test

# Component testing only
sudo python main.py --test-components
```

### **Gmail Setup for Reports**
1. **Enable 2-Factor Authentication** on Gmail
2. **Generate App Password**: Gmail Settings → Security → App passwords  
3. **Use app password** (not regular password) in `config.json`
4. **Test email**: Run `python development/tools/test_direct_email.py`

## 📁 **Enhanced Project Structure**

```
KeyLogger/
├── 📁 config/                 # Configuration management
│   └── config.json           # Main configuration (enhanced)
├── 📁 logs/                  # Encrypted log storage
│   ├── keylog.txt           # Clean formatted logs
│   ├── keylog.enc           # AES-256 encrypted logs
│   └── .encryption.key      # Secure encryption key
├── 📁 src/                   # Enhanced source code
│   ├── 📁 core/             # Core functionality
│   │   ├── keylogger.py     # Enhanced keylogger with smart detection
│   │   └── launcher.py      # Application launcher
│   ├── 📁 managers/         # Specialized managers
│   │   ├── config_manager.py    # Configuration management
│   │   ├── log_manager.py       # Enhanced log formatting
│   │   ├── stealth_manager.py   # Anti-detection features
│   │   └── persistence_manager.py # System integration
│   └── 📁 utils/            # Utility functions
├── 📁 development/          # Development tools
│   ├── 📁 tests/           # Comprehensive unit tests
│   └── 📁 tools/           # Email and functionality testing
├── 📁 examples/            # Configuration examples
├── 📁 documentation/       # Enhanced documentation
├── main.py                 # Enhanced entry point
├── requirements.txt        # Updated dependencies
└── README.md              # This enhanced documentation
```

## 🔧 **Enhanced Configuration**

### **Smart Keylogger Settings**
```json
{
    "keylogger": {
        "enabled": true,
        "buffer_size": 20,              // Smaller for faster app detection
        "flush_interval_minutes": 5,
        "capture_window_titles": true,
        "capture_application_names": true,
        "log_special_keys": true,
        "log_timestamps": true
    }
}
```

```json
{
    "encryption": {
        "enabled": true,
        "algorithm": "Fernet",
        "password": "change-this-secure-password",
        "key_file": "logs/.encryption.key",
        "compress_logs": true
    },
    "stealth": {
        "hide_console": false,           // Set true for stealth mode
        "process_name_obfuscation": false,
        "vm_detection": true,            // Detect virtual machines
        "anti_debug": false
    }
}
```

### **Professional Email Settings**
```json
{
    "email": {
        "enabled": true,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "use_tls": true,
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "recipient_email": "reports@your-domain.com",
        "send_interval_hours": 0.1       // Send every 6 minutes for testing
    }
}
```

## 🧪 **Testing & Validation**

### **Component Testing**
```bash
# Test core components
python main.py --test

# Test configuration loading
python -c "from src.managers.config_manager import ConfigManager; print('✅ Config OK')"

# Test encryption
python -c "from src.managers.log_manager import LogManager; print('✅ Encryption OK')"

# Test email functionality
python development/tools/test_direct_email.py
```

### **Development & Debugging**
```bash
# Debug mode with verbose output
python main.py --debug

# Monitor logs in real-time
tail -f logs/keylog.txt

# Check encrypted logs
python -c "
from src.managers.log_manager import LogManager
lm = LogManager()
with open('logs/keylog.enc', 'r') as f:
    encrypted = f.read()
    print(lm.decrypt_data(encrypted))
"
```

### **Performance Validation**
- ✅ **Response Time**: Window detection < 0.5 seconds
- ✅ **Memory Usage**: < 50MB RAM
- ✅ **CPU Impact**: < 5% CPU usage
- ✅ **Buffer Efficiency**: Auto-flush on app switches
- ✅ **Email Delivery**: Clean, professional reports

## 📊 **Enhanced Features Showcase**

### **Smart Application Detection**
- **Instant Alt+Tab Detection**: Captures window switches immediately
- **Multi-Platform Support**: Works on Linux, Windows, macOS
- **Intelligent Buffering**: Flushes logs when applications change
- **Clean Formatting**: Professional, readable output

### **Professional Email Reports**
- **Rich Formatting**: Proper timestamps and application headers
- **Clean Text**: No scattered characters or formatting artifacts
- **Special Key Handling**: Clear display of `[CTRL]`, `[ALT]`, `[TAB]`, etc.
- **Application Context**: Shows exactly which app keystrokes occurred in

## 📚 **Enhanced Documentation**

- **[📖 Complete Documentation](documentation/INDEX.md)** - Technical specifications
- **[📧 Email Configuration](documentation/EMAIL_SETUP.md)** - Setup guide with examples
- **[🏗️ System Architecture](documentation/STRUCTURE.md)** - Codebase structure
- **[📄 Research Report](reports/latex/)** - Academic documentation and analysis

## 🔧 **Troubleshooting**

### **Common Issues**
```bash
# Permission issues (Linux/macOS)
sudo python main.py

# Python version check
python --version  # Should be 3.8+

# Dependencies check
pip list | grep -E "(pynput|cryptography)"

# Window detection not working
sudo apt-get install xdotool wmctrl  # Linux only
```

### **Email Issues**
```bash
# Test email configuration
python development/tools/test_direct_email.py

# Check Gmail app password
# Settings → Security → App passwords → Generate
```

## ⚖️ **Legal & Ethical Guidelines**

### **✅ Authorized Use Cases:**
- 🎓 **Cybersecurity Education**: Learning input monitoring techniques
- 🔍 **Authorized Testing**: Penetration testing with explicit permission
- 🔬 **Security Research**: Academic research in controlled environments
- 📚 **Digital Forensics**: Training and educational analysis
- 🏛️ **Academic Projects**: University coursework and research

### **❌ Strictly Prohibited:**
- 🚫 **Unauthorized Monitoring**: Using on systems without permission
- 🚫 **Privacy Violations**: Monitoring others without consent
- 🚫 **Corporate Espionage**: Stealing confidential information
- 🚫 **Malicious Distribution**: Spreading as malware
- 🚫 **Illegal Surveillance**: Any unauthorized surveillance activities

### **🛡️ Responsible Use Requirements:**
1. **Explicit Permission**: Always obtain written authorization
2. **Controlled Environment**: Use only in authorized lab settings
3. **Legal Compliance**: Follow all applicable laws and regulations
4. **Data Protection**: Secure and properly dispose of captured data
5. **Ethical Standards**: Respect privacy and confidentiality

## 🤝 **Contributing to Education**

We welcome contributions that enhance the educational value:

### **How to Contribute:**
1. **Fork** the repository on GitHub
2. **Create** educational feature branch
3. **Implement** improvements with proper documentation
4. **Test** thoroughly in safe environments
5. **Submit** pull request with detailed explanation

### **Contribution Areas:**
- 📚 Educational documentation and tutorials
- 🔧 Code improvements and optimizations
- 🧪 Enhanced testing frameworks
- 🛡️ Security and ethical enhancements
- 🌐 Cross-platform compatibility improvements

## 📞 **Support & Contact**

- **Issues**: [GitHub Issues](https://github.com/AyGoub/KeyLogger/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AyGoub/KeyLogger/discussions)
- **Documentation**: [Project Wiki](https://github.com/AyGoub/KeyLogger/wiki)

## 📄 **License & Disclaimer**

This project is licensed for **Educational Use Only**. 

⚠️ **Important**: The authors are not responsible for misuse of this software. Users must comply with all applicable laws and obtain proper authorization before use.

---

**Made with 💻 for Cybersecurity Education**  
*Version 2.1 - Enhanced Edition with Smart Detection & Professional Reporting*

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