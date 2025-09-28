# Educational Keylogger Project Structure

This document explains the organized directory structure of the educational keylogger project.

## Directory Structure

```
KeyLogger/
├── main.py                     # Main entry point for the application
├── requirements.txt            # Python dependencies
├── 
├── src/                        # Source code directory
│   ├── __init__.py            # Package initialization
│   ├── core/                  # Core application components
│   │   ├── __init__.py       # Core package initialization
│   │   ├── keylogger.py      # Main keylogger class and functionality
│   │   └── launcher.py       # Application launcher with CLI interface
│   ├── managers/              # Specialized manager classes
│   │   ├── __init__.py       # Managers package initialization
│   │   ├── config_manager.py # Configuration handling
│   │   ├── log_manager.py    # Logging and encryption management
│   │   ├── persistence_manager.py # Startup persistence management
│   │   └── stealth_manager.py # Anti-detection and stealth features
│   └── utils/                 # Utility functions (for future expansion)
│       └── __init__.py       # Utils package initialization
│
├── config/                    # Configuration files
│   └── config.json           # Main configuration file
│
├── docs/                      # Documentation
│   └── README.md             # Main project documentation
│
├── build_tools/              # Build and deployment tools
│   ├── build.py              # PyInstaller build script
│   └── setup.sh              # Environment setup script
│
├── tests/                    # Unit tests (for future implementation)
├── examples/                 # Example configurations and use cases
└── logs/                     # Generated log files (created at runtime)
```

## Component Overview

### Core Components (`src/core/`)
- **keylogger.py**: The main keylogger implementation with keystroke capture
- **launcher.py**: CLI interface and application entry point with argument parsing

### Managers (`src/managers/`)
- **config_manager.py**: Handles configuration loading, validation, and monitoring
- **log_manager.py**: Manages log encryption, storage, and export functionality
- **persistence_manager.py**: Handles startup persistence mechanisms
- **stealth_manager.py**: Implements anti-detection and stealth features

### Configuration (`config/`)
- **config.json**: Main configuration file with all settings

### Build Tools (`build_tools/`)
- **build.py**: Automated PyInstaller script for creating executables
- **setup.sh**: Environment setup and dependency installation

### Documentation (`docs/`)
- **README.md**: Comprehensive project documentation and usage guide

## Usage

### Quick Start
```bash
# Run from project root
python main.py

# Or run directly with launcher
python src/core/launcher.py
```

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (when implemented)
python -m pytest tests/

# Build executable
python build_tools/build.py
```

## Benefits of This Structure

1. **Separation of Concerns**: Each component has a clear responsibility
2. **Maintainability**: Easy to locate and modify specific functionality
3. **Scalability**: Easy to add new features in appropriate directories
4. **Professional**: Follows Python project best practices
5. **Educational**: Clear structure helps understand software architecture
6. **Reusability**: Components can be imported and reused independently

## Import Structure

The new directory structure uses proper Python packages with relative imports:

```python
# From main.py or external scripts
from src.core.keylogger import StealthKeylogger
from src.managers.config_manager import ConfigManager

# Within the package
from ..managers.log_manager import LogManager
```

This organization makes the project more professional and easier to understand for educational purposes.