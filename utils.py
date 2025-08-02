#!/usr/bin/env python3
"""
Utilities for the Autocomplete System

This module provides auxiliary functions and tools for the autocomplete
system, including validation, formatting, and system utilities.

Author: Team 3
Date: 2024
"""

import os
import sys
import time
import psutil
import logging
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
import yaml
from datetime import datetime


class SystemUtils:
    """System utilities"""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """
        Gets system information
        
        Returns:
            Dictionary with system information
        """
        return {
            'platform': sys.platform,
            'python_version': sys.version,
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'disk_usage': psutil.disk_usage('/').percent
        }
    
    @staticmethod
    def check_system_requirements() -> Tuple[bool, List[str]]:
        """
        Verifies that the system meets minimum requirements
        
        Returns:
            Tuple with (meets_requirements, list_of_errors)
        """
        errors = []
        
        # Check Python version
        if sys.version_info < (3, 8):
            errors.append("Python 3.8 or higher is required")
        
        # Check available memory
        memory_gb = psutil.virtual_memory().available / (1024**3)
        if memory_gb < 2:
            errors.append(f"At least 2GB of RAM is required. Available: {memory_gb:.1f}GB")
        
        # Check disk space
        disk_free_gb = psutil.disk_usage('/').free / (1024**3)
        if disk_free_gb < 1:
            errors.append(f"At least 1GB of free space is required. Available: {disk_free_gb:.1f}GB")
        
        return len(errors) == 0, errors


class ConfigManager:
    """Configuration manager"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initializes the configuration manager
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Loads configuration from YAML file
        
        Returns:
            Dictionary with configuration
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as file:
                    return yaml.safe_load(file)
            else:
                logging.warning(f"Configuration file not found: {self.config_path}")
                return self._get_default_config()
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Returns default configuration"""
        return {
            'data': {
                'directory': './Archive',
                'file_extensions': ['.txt'],
                'encoding': 'utf-8'
            },
            'performance': {
                'max_memory_mb': 4096,
                'batch_size': 1000
            },
            'scoring': {
                'max_results': 5
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/application.log'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Gets a configuration value
        
        Args:
            key: Configuration key (can use dot notation)
            default: Default value if not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Sets a configuration value
        
        Args:
            key: Configuration key
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self) -> None:
        """Saves configuration to file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(self.config, file, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")


class TextUtils:
    """Text processing utilities"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans and normalizes text
        
        Args:
            text: Text to clean
            
        Returns:
            Clean and normalized text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Normalize spaces
        text = ' '.join(text.split())
        
        return text
    
    @staticmethod
    def split_sentences(text: str) -> List[str]:
        """
        Splits text into sentences
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        import re
        
        # Pattern to split sentences
        sentence_pattern = r'[.!?]+'
        sentences = re.split(sentence_pattern, text)
        
        # Clean and filter empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        Calculates similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity value between 0 and 1
        """
        if not text1 or not text2:
            return 0.0
        
        # Convert to word sets
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0

    @staticmethod
    def validate_input(text: str, min_length: int = 1, max_length: int = 1000) -> Tuple[bool, str]:
        """
        Validates user input text
        
        Args:
            text: Text to validate
            min_length: Minimum allowed length
            max_length: Maximum allowed length
            
        Returns:
            Tuple with (is_valid, error_message)
        """
        if not text:
            return False, "Input cannot be empty"
        
        if len(text) < min_length:
            return False, f"Input must be at least {min_length} characters long"
        
        if len(text) > max_length:
            return False, f"Input cannot exceed {max_length} characters"
        
        # Check for valid characters (letters, numbers, spaces, basic punctuation)
        import re
        if not re.match(r'^[a-zA-Z0-9\s.,!?-]+$', text):
            return False, "Input contains invalid characters"
        
        return True, ""
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """
        Formats file size in human readable format
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string
        """
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    @staticmethod
    def get_system_stats() -> Dict[str, Any]:
        """
        Gets comprehensive system statistics
        
        Returns:
            Dictionary with system statistics
        """
        import platform
        
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'disk_free': psutil.disk_usage('/').free
        }


class FileUtils:
    """File handling utilities"""
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """
        Gets file information
        
        Args:
            file_path: File path
            
        Returns:
            Dictionary with file information
        """
        try:
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'created': datetime.fromtimestamp(stat.st_ctime),
                'extension': Path(file_path).suffix,
                'name': Path(file_path).name
            }
        except Exception as e:
            logging.error(f"Error getting file information for {file_path}: {e}")
            return {}
    
    @staticmethod
    def get_files_by_extension(directory: str, extensions: List[str]) -> List[str]:
        """
        Gets files by extension
        
        Args:
            directory: Directory to search
            extensions: List of extensions to search for
            
        Returns:
            List of file paths
        """
        files = []
        
        try:
            for root, dirs, filenames in os.walk(directory):
                for filename in filenames:
                    if any(filename.endswith(ext) for ext in extensions):
                        files.append(os.path.join(root, filename))
        except Exception as e:
            logging.error(f"Error searching files in {directory}: {e}")
        
        return files
    
    @staticmethod
    def safe_read_file(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
        """
        Safely reads a file
        
        Args:
            file_path: File path
            encoding: File encoding
            
        Returns:
            File content or None if error
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                # Try with another encoding
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                logging.error(f"Error reading file {file_path}: {e}")
                return None
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return None


class PerformanceMonitor:
    """Performance monitor"""
    
    def __init__(self):
        """Initializes the performance monitor"""
        self.start_time = None
        self.memory_start = None
    
    def start(self) -> None:
        """Starts monitoring"""
        self.start_time = time.time()
        self.memory_start = psutil.Process().memory_info().rss
    
    def stop(self) -> Dict[str, float]:
        """
        Stops monitoring and returns metrics
        
        Returns:
            Dictionary with performance metrics
        """
        if self.start_time is None:
            return {}
        
        end_time = time.time()
        memory_end = psutil.Process().memory_info().rss
        
        return {
            'execution_time': end_time - self.start_time,
            'memory_used_mb': (memory_end - self.memory_start) / (1024 * 1024),
            'memory_total_mb': memory_end / (1024 * 1024)
        }
    
    @staticmethod
    def get_current_memory_usage() -> float:
        """
        Gets current memory usage
        
        Returns:
            Memory usage in MB
        """
        return psutil.Process().memory_info().rss / (1024 * 1024)


class ProgressBar:
    """Simple progress bar"""
    
    def __init__(self, total: int, description: str = "Processing"):
        """
        Initializes the progress bar
        
        Args:
            total: Total elements to process
            description: Process description
        """
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
    
    def update(self, increment: int = 1) -> None:
        """
        Updates progress
        
        Args:
            increment: Progress increment
        """
        self.current += increment
        self._display()
    
    def _display(self) -> None:
        """Displays the progress bar"""
        if self.total == 0:
            return
        
        percentage = (self.current / self.total) * 100
        elapsed_time = time.time() - self.start_time
        
        # Calculate estimated remaining time
        if self.current > 0:
            estimated_total = elapsed_time * self.total / self.current
            remaining_time = estimated_total - elapsed_time
            eta_str = f"ETA: {remaining_time:.1f}s"
        else:
            eta_str = "ETA: --"
        
        # Create visual bar
        bar_length = 30
        filled_length = int(bar_length * self.current // self.total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        print(f"\r{self.description}: |{bar}| {percentage:.1f}% ({self.current}/{self.total}) {eta_str}", end='', flush=True)
    
    def finish(self) -> None:
        """Finishes the progress bar"""
        self.current = self.total
        self._display()
        print()  # New line at the end


# Global instances for easy use
config_manager = ConfigManager()
performance_monitor = PerformanceMonitor() 