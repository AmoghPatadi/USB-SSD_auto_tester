"""
Device Manager for USB/SSD Storage Testing

This module handles device detection, validation, and information gathering
for storage devices on different operating systems.
"""

import os
import platform
import psutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DeviceManager:
    """Manages storage device operations and validation."""
    
    def __init__(self):
        self.system = platform.system()
        
    def list_storage_devices(self):
        """
        List all available removable storage devices.
        
        Returns:
            list: List of device dictionaries with device information
        """
        devices = []
        
        try:
            if self.system == "Windows":
                devices = self._list_windows_devices()
            elif self.system in ["Linux", "Darwin"]:
                devices = self._list_unix_devices()
            else:
                logger.warning(f"Unsupported operating system: {self.system}")
                
        except Exception as e:
            logger.error(f"Error listing storage devices: {str(e)}")
            
        return devices
    
    def _list_windows_devices(self):
        """List removable storage devices on Windows."""
        devices = []
        
        for partition in psutil.disk_partitions():
            if 'removable' in partition.opts or partition.fstype in ['FAT32', 'NTFS', 'exFAT']:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    device_info = {
                        'path': partition.mountpoint,
                        'device': partition.device,
                        'file_system': partition.fstype,
                        'label': self._get_volume_label(partition.mountpoint),
                        'size_bytes': usage.total,
                        'size_gb': usage.total / (1024**3),
                        'free_bytes': usage.free,
                        'free_gb': usage.free / (1024**3),
                        'used_bytes': usage.used,
                        'used_gb': usage.used / (1024**3),
                        'is_removable': 'removable' in partition.opts
                    }
                    devices.append(device_info)
                except PermissionError:
                    logger.warning(f"Permission denied accessing {partition.mountpoint}")
                except Exception as e:
                    logger.warning(f"Error accessing {partition.mountpoint}: {str(e)}")
                    
        return devices
    
    def _list_unix_devices(self):
        """List removable storage devices on Unix-like systems."""
        devices = []
        
        for partition in psutil.disk_partitions():
            # Check if it's a removable device (USB, external drive, etc.)
            if (partition.device.startswith('/dev/sd') or 
                partition.device.startswith('/dev/disk') or
                '/media/' in partition.mountpoint or
                '/mnt/' in partition.mountpoint):
                
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    device_info = {
                        'path': partition.mountpoint,
                        'device': partition.device,
                        'file_system': partition.fstype,
                        'label': os.path.basename(partition.mountpoint),
                        'size_bytes': usage.total,
                        'size_gb': usage.total / (1024**3),
                        'free_bytes': usage.free,
                        'free_gb': usage.free / (1024**3),
                        'used_bytes': usage.used,
                        'used_gb': usage.used / (1024**3),
                        'is_removable': True
                    }
                    devices.append(device_info)
                except PermissionError:
                    logger.warning(f"Permission denied accessing {partition.mountpoint}")
                except Exception as e:
                    logger.warning(f"Error accessing {partition.mountpoint}: {str(e)}")
                    
        return devices
    
    def _get_volume_label(self, drive_path):
        """Get volume label for Windows drives."""
        try:
            import subprocess
            result = subprocess.run(
                ['vol', drive_path],
                capture_output=True,
                text=True,
                shell=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'Volume in drive' in line and 'is' in line:
                        return line.split('is')[-1].strip()
            return "Unknown"
        except Exception:
            return "Unknown"
    
    def validate_device(self, device_path):
        """
        Validate that a device path is accessible and writable.
        
        Args:
            device_path (str): Path to the device to validate
            
        Returns:
            bool: True if device is valid and accessible, False otherwise
        """
        try:
            # Check if path exists
            if not os.path.exists(device_path):
                logger.error(f"Device path does not exist: {device_path}")
                return False
            
            # Check if it's a directory (mount point)
            if not os.path.isdir(device_path):
                logger.error(f"Device path is not a directory: {device_path}")
                return False
            
            # Check if we have write permissions
            test_file = os.path.join(device_path, '.storage_test_write_check')
            try:
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                logger.info(f"Device validation successful: {device_path}")
                return True
            except (PermissionError, OSError) as e:
                logger.error(f"Cannot write to device {device_path}: {str(e)}")
                return False
                
        except Exception as e:
            logger.error(f"Error validating device {device_path}: {str(e)}")
            return False
    
    def get_device_info(self, device_path):
        """
        Get detailed information about a specific device.
        
        Args:
            device_path (str): Path to the device
            
        Returns:
            dict: Device information dictionary
        """
        try:
            usage = psutil.disk_usage(device_path)
            
            # Find matching partition info
            partition_info = None
            for partition in psutil.disk_partitions():
                if partition.mountpoint == device_path:
                    partition_info = partition
                    break
            
            device_info = {
                'path': device_path,
                'device': partition_info.device if partition_info else 'Unknown',
                'file_system': partition_info.fstype if partition_info else 'Unknown',
                'label': self._get_volume_label(device_path) if self.system == "Windows" else os.path.basename(device_path),
                'size_bytes': usage.total,
                'size_gb': usage.total / (1024**3),
                'free_bytes': usage.free,
                'free_gb': usage.free / (1024**3),
                'used_bytes': usage.used,
                'used_gb': usage.used / (1024**3),
                'usage_percent': (usage.used / usage.total) * 100 if usage.total > 0 else 0
            }
            
            return device_info
            
        except Exception as e:
            logger.error(f"Error getting device info for {device_path}: {str(e)}")
            return None
    
    def get_available_space(self, device_path):
        """
        Get available space on device in bytes.
        
        Args:
            device_path (str): Path to the device
            
        Returns:
            int: Available space in bytes, or None if error
        """
        try:
            usage = psutil.disk_usage(device_path)
            return usage.free
        except Exception as e:
            logger.error(f"Error getting available space for {device_path}: {str(e)}")
            return None
    
    def is_device_mounted(self, device_path):
        """
        Check if a device is currently mounted and accessible.
        
        Args:
            device_path (str): Path to the device
            
        Returns:
            bool: True if device is mounted, False otherwise
        """
        try:
            return os.path.exists(device_path) and os.path.ismount(device_path)
        except Exception:
            return False
