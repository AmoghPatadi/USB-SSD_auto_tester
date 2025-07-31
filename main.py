#!/usr/bin/env python3
"""
USB/SSD Storage Device Validation Framework
Main Entry Point

This is the main entry point for the storage device testing framework.
It provides a command-line interface for running various types of tests
on USB and SSD storage devices.
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.test_framework import StorageTestFramework
from src.core.config_manager import ConfigManager
from src.core.device_manager import DeviceManager
from src.reporting.report_generator import ReportGenerator
from src.utils.logger import setup_logging

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="USB/SSD Storage Device Validation Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --device E: --test performance
  %(prog)s --device F: --test all --iterations 10
  %(prog)s --list-devices
  %(prog)s --config custom_config.yaml --test endurance
        """
    )
    
    parser.add_argument(
        '--device', '-d',
        type=str,
        help='Target device path (e.g., E:, F:, /dev/sdb1)'
    )
    
    parser.add_argument(
        '--test', '-t',
        choices=['performance', 'integrity', 'endurance', 'fault', 'all'],
        default='all',
        help='Type of test to run (default: all)'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        default='config.yaml',
        help='Configuration file path (default: config.yaml)'
    )
    
    parser.add_argument(
        '--iterations', '-i',
        type=int,
        help='Number of test iterations (overrides config)'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        help='Output directory for reports (overrides config)'
    )
    
    parser.add_argument(
        '--list-devices', '-l',
        action='store_true',
        help='List available storage devices'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--dashboard',
        action='store_true',
        help='Start web dashboard for real-time monitoring'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without actual testing'
    )
    
    return parser.parse_args()

def list_devices():
    """List available storage devices."""
    print("🔍 Scanning for available storage devices...")
    device_manager = DeviceManager()
    devices = device_manager.list_storage_devices()
    
    if not devices:
        print("❌ No removable storage devices found.")
        return
    
    print(f"✅ Found {len(devices)} storage device(s):")
    for i, device in enumerate(devices, 1):
        print(f"  {i}. {device['path']} - {device['label']} "
              f"({device['size_gb']:.1f} GB, {device['file_system']})")

def main():
    """Main function."""
    args = parse_arguments()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Starting USB/SSD Storage Device Validation Framework")
    
    # List devices if requested
    if args.list_devices:
        list_devices()
        return 0
    
    try:
        # Load configuration
        config_manager = ConfigManager(args.config)
        config = config_manager.get_config()
        
        # Override config with command line arguments
        if args.iterations:
            config['test_parameters']['iterations'] = args.iterations
        if args.output_dir:
            config['reporting']['output_dir'] = args.output_dir
        
        # Validate device
        if not args.device:
            logger.error("❌ No device specified. Use --device or --list-devices")
            return 1
        
        device_manager = DeviceManager()
        if not device_manager.validate_device(args.device):
            logger.error(f"❌ Invalid or inaccessible device: {args.device}")
            return 1
        
        # Initialize test framework
        framework = StorageTestFramework(config, args.device)
        
        if args.dry_run:
            logger.info("🧪 Performing dry run...")
            framework.dry_run()
            return 0
        
        # Start dashboard if requested
        if args.dashboard:
            logger.info("🌐 Starting web dashboard...")
            # Dashboard implementation would go here
            pass
        
        # Run tests
        logger.info(f"🧪 Starting {args.test} test(s) on device: {args.device}")
        
        results = None
        if args.test == 'all':
            results = framework.run_all_tests()
        elif args.test == 'performance':
            results = framework.run_performance_tests()
        elif args.test == 'integrity':
            results = framework.run_integrity_tests()
        elif args.test == 'endurance':
            results = framework.run_endurance_tests()
        elif args.test == 'fault':
            results = framework.run_fault_tests()
        
        # Generate reports
        if results:
            logger.info("📊 Generating test reports...")
            report_generator = ReportGenerator(config)
            report_generator.generate_reports(results)
            
            # Print summary
            print("\n" + "="*60)
            print("📋 TEST SUMMARY")
            print("="*60)
            print(f"Device: {args.device}")
            print(f"Test Type: {args.test}")
            print(f"Total Tests: {results.get('total_tests', 0)}")
            print(f"Passed: {results.get('passed', 0)}")
            print(f"Failed: {results.get('failed', 0)}")
            print(f"Success Rate: {results.get('success_rate', 0):.1f}%")
            
            if results.get('failed', 0) > 0:
                print(f"⚠️  {results.get('failed', 0)} test(s) failed!")
                return 1
            else:
                print("✅ All tests passed!")
        
        logger.info("🎉 Testing completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        logger.warning("⚠️  Testing interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
