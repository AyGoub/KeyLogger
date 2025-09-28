#!/usr/bin/env python3
"""
Direct Email Test
================
Test Gmail SMTP connection directly without the keylogger wrapper
"""

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def test_direct_email():
    """Test email sending directly"""
    
    # Load config
    with open('examples/email_demo_config.json', 'r') as f:
        config = json.load(f)
    
    email_config = config['email']
    
    print("🔧 Testing Direct SMTP Connection")
    print("=" * 40)
    print(f"📤 Sender: {email_config['sender_email']}")
    print(f"📥 Recipient: {email_config['recipient_email']}")
    print(f"🌐 Server: {email_config['smtp_server']}:{email_config['smtp_port']}")
    print(f"🔒 TLS: {email_config['use_tls']}")
    
    try:
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = email_config['sender_email']
        msg['To'] = email_config['recipient_email']
        msg['Subject'] = f"🧪 Direct Email Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        body = f"""
🧪 Educational Keylogger Email Test
================================

This is a direct SMTP test to verify your Gmail configuration.

Test Details:
- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Sender: {email_config['sender_email']}
- SMTP Server: {email_config['smtp_server']}:{email_config['smtp_port']}

If you receive this email, your configuration is working correctly!

Next steps:
1. ✅ Gmail SMTP is working
2. 🔄 Test keylogger email integration
3. 📊 Set up automatic reporting

Educational purposes only - use responsibly!
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        print("\n🔌 Connecting to SMTP server...")
        server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
        
        print("🔒 Starting TLS encryption...")
        server.starttls()
        
        print("🔐 Authenticating...")
        server.login(email_config['sender_email'], email_config['sender_password'])
        
        print("📧 Sending email...")
        text = msg.as_string()
        server.sendmail(email_config['sender_email'], email_config['recipient_email'], text)
        
        print("🔌 Closing connection...")
        server.quit()
        
        print("\n✅ SUCCESS! Email sent successfully!")
        print("📬 Check your inbox (and spam folder)")
        print("📊 If you received the email, your Gmail setup is working perfectly!")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION ERROR: {e}")
        print("🔐 This means your email/password is incorrect")
        print("💡 Solutions:")
        print("   1. Make sure 2-factor authentication is enabled")
        print("   2. Use App Password (not regular password)")
        print("   3. Generate new App Password: https://myaccount.google.com/apppasswords")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("🌐 Cannot connect to Gmail SMTP server")
        print("💡 Solutions:")
        print("   1. Check internet connection")
        print("   2. Check firewall settings")
        print("   3. Try different network (maybe VPN blocking SMTP)")
        return False
        
    except smtplib.SMTPServerDisconnected as e:
        print(f"\n❌ SERVER DISCONNECTED: {e}")
        print("🔌 Connection was lost during the process")
        print("💡 Solutions:")
        print("   1. Check network stability")
        print("   2. Try again in a few minutes")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        print("💡 This might be a configuration or network issue")
        return False

if __name__ == "__main__":
    test_direct_email()