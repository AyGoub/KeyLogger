"""
Unit tests for ConfigManager class

These tests verify the configuration management functionality
including loading, validation, and error handling.
"""

import unittest
import tempfile
import json
import os
from pathlib import Path

# Import the module to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.managers.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager class"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_config = {
            "keylogger": {
                "enabled": True,
                "log_file": "test.txt",
                "encrypted_log_file": "test.enc",
                "log_special_keys": True,
                "debug_mode": False
            },
            "encryption": {
                "enabled": True,
                "key_file": "test.key",
                "algorithm": "AES-256"
            }
        }
        
        # Create temporary config file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_config, self.temp_file)
        self.temp_file.close()
        
    def tearDown(self):
        """Clean up after each test method."""
        os.unlink(self.temp_file.name)
        
    def test_load_config(self):
        """Test loading configuration from file"""
        config_manager = ConfigManager(self.temp_file.name)
        loaded_config = config_manager.get_config()
        
        self.assertEqual(loaded_config['keylogger']['enabled'], True)
        self.assertEqual(loaded_config['keylogger']['log_file'], 'test.txt')
        
    def test_config_validation(self):
        """Test configuration validation"""
        config_manager = ConfigManager(self.temp_file.name)
        
        # Should not raise an exception for valid config
        try:
            config_manager.validate_config()
        except Exception as e:
            self.fail(f"validate_config() raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()