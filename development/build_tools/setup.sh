#!/bin/bash

# Educational Keylogger Setup Script
# For Linux/Unix systems

echo "🔧 Educational Keylogger Setup"
echo "=============================="
echo "⚠️  For Educational Use Only ⚠️"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python version: $PYTHON_VERSION"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed"
    echo "Please install pip3"
    exit 1
fi

echo "✅ pip3 is available"

# Check if we need a virtual environment (Kali Linux and similar)
USE_VENV=false
if pip3 install --help 2>&1 | grep -q "externally-managed-environment" || python3 -c "import sys; exit(0 if hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix else 1)" 2>/dev/null; then
    echo "⚠️  Externally managed Python environment detected"
    USE_VENV=true
fi

# Create virtual environment (recommended for Kali Linux)
if [ "$USE_VENV" = true ]; then
    echo "📦 Creating virtual environment (required)..."
    python3 -m venv keylogger_env
    source keylogger_env/bin/activate
    echo "✅ Virtual environment created and activated"
    PIP_CMD="pip"
else
    read -p "Create virtual environment? (y/N): " create_venv
    if [[ $create_venv =~ ^[Yy]$ ]]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv keylogger_env
        source keylogger_env/bin/activate
        echo "✅ Virtual environment created and activated"
        PIP_CMD="pip"
    else
        PIP_CMD="pip3"
    fi
fi

# Install requirements
echo "📥 Installing requirements..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Requirements installed successfully"
else
    echo "❌ Failed to install requirements"
    exit 1
fi

# Make scripts executable
echo "🔐 Setting permissions..."
chmod +x launcher.py
chmod +x keylogger.py
chmod +x build.py
echo "✅ Permissions set"

# Test installation
echo "🧪 Testing installation..."
if [ -f "keylogger_env/bin/activate" ]; then
    source keylogger_env/bin/activate
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

$PYTHON_CMD launcher.py --test

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    if [ -f "keylogger_env/bin/activate" ]; then
        echo "Usage (with virtual environment):"
        echo "  source keylogger_env/bin/activate"
        echo "  python launcher.py               # Start keylogger"
        echo "  python launcher.py --test        # Test components"  
        echo "  python launcher.py --help        # Show help"
        echo ""
        echo "Or create a convenience script:"
        echo "  echo '#!/bin/bash' > run.sh"
        echo "  echo 'source keylogger_env/bin/activate && python launcher.py \"\$@\"' >> run.sh"
        echo "  chmod +x run.sh"
        echo "  ./run.sh --help"
    else
        echo "Usage:"
        echo "  python3 launcher.py          # Start keylogger"
        echo "  python3 launcher.py --test   # Test components"  
        echo "  python3 launcher.py --help   # Show help"
    fi
    echo ""
    echo "⚠️  Remember: Educational use only!"
else
    echo "❌ Installation test failed"
    exit 1
fi