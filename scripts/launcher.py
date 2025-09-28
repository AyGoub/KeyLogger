#!/usr/bin/env python3
"""
Main Entry Point for Educational Keylogger
==========================================

This script provides a simple entry point to run the keylogger
from the project root directory.

Usage:
    python main.py [arguments]
    
For help:
    python main.py --help
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Import and run the main launcher
if __name__ == "__main__":
    try:
        from src.core.launcher import main
        main()
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Keylogger stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)