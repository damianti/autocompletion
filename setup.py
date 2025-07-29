#!/usr/bin/env python3
"""
Autocomplete System Installation Script

This script automates the installation and configuration of the autocomplete
system, checking dependencies and setting up the environment.

Author: Team 3
Date: 2024
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_banner():
    """Prints the installation banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🚀 Intelligent Autocomplete System                       ║
    ║                                                              ║
    ║    Automatic Installer                                       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """Checks Python version"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def check_pip():
    """Checks if pip is available"""
    print("🔍 Checking pip...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error: pip is not available")
        return False


def create_virtual_environment():
    """Creates a Python virtual environment"""
    print("🐍 Creating virtual environment...")
    
    venv_name = "venv"
    
    try:
        # Check if virtual environment already exists
        if os.path.exists(venv_name):
            print(f"   ⚠️  Virtual environment '{venv_name}' already exists")
            return True
        
        # Create virtual environment
        subprocess.run([
            sys.executable, "-m", "venv", venv_name
        ], check=True)
        
        print(f"   ✅ Virtual environment '{venv_name}' created successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error creating virtual environment: {e}")
        return False


def get_venv_python():
    """Gets the Python executable from the virtual environment"""
    if sys.platform == "win32":
        return os.path.join("venv", "Scripts", "python.exe")
    else:
        return os.path.join("venv", "bin", "python")


def install_dependencies():
    """Installs project dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Get virtual environment Python
        venv_python = get_venv_python()
        
        # Upgrade pip first
        subprocess.run([
            venv_python, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True)
        
        # Install main dependencies
        subprocess.run([
            venv_python, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def create_directories():
    """Creates necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "logs",
        "data",
        "tests",
        "docs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ Created: {directory}/")
    
    return True


def check_data_directory():
    """Checks if the data directory exists"""
    print("📂 Checking data directory...")
    
    archive_dir = Path("Archive")
    if not archive_dir.exists():
        print("⚠️  Warning: 'Archive' directory does not exist")
        print("   The system will work with example data")
        
        # Create example file
        example_file = archive_dir / "example.txt"
        archive_dir.mkdir(exist_ok=True)
        
        with open(example_file, "w", encoding="utf-8") as f:
            f.write("This is an example sentence for testing.\n")
            f.write("The autocomplete system will use this data.\n")
            f.write("Network protocols are important for communication.\n")
        
        print(f"   ✅ Created example file: {example_file}")
    else:
        print("✅ Data directory found")
    
    return True


def run_tests():
    """Runs basic tests"""
    print("🧪 Running basic tests...")
    
    try:
        # Test basic imports
        import pandas
        import psutil
        print("   ✅ Basic imports working")
        
        # Test project modules
        from Trie import Trie
        from calculate_score import ScoreCalculator
        print("   ✅ Project modules working")
        
        # Basic Trie test
        trie = Trie()
        trie.insert("test", 1, 0)
        sentences = trie.get_sentences_of_word("test")
        if sentences and 1 in sentences:
            print("   ✅ Trie structure working")
        else:
            print("   ⚠️  Warning: Trie test failed")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        return False


def create_startup_script():
    """Creates startup script"""
    print("🚀 Creating startup script...")
    
    if sys.platform == "win32":
        script_content = """@echo off
echo Starting Intelligent Autocomplete System...
call venv\\Scripts\\activate
python main.py
pause
"""
        script_name = "start.bat"
    else:
        script_content = """#!/bin/bash
echo "🚀 Starting Intelligent Autocomplete System..."
source venv/bin/activate
python main.py
"""
        script_name = "start.sh"
    
    with open(script_name, "w", encoding="utf-8") as f:
        f.write(script_content)
    
    if sys.platform != "win32":
        os.chmod(script_name, 0o755)
    
    print(f"   ✅ Created: {script_name}")
    return True


def show_usage_instructions():
    """Shows usage instructions"""
    print("\n" + "="*60)
    print("🎉 Installation Completed!")
    print("="*60)
    
    print("\n📋 To use the system:")
    
    if sys.platform == "win32":
        print("   • Run: start.bat")
        print("   • Or directly: venv\\Scripts\\python main.py")
    else:
        print("   • Run: ./start.sh")
        print("   • Or directly: venv/bin/python main.py")
    
    print("\n📚 Available resources:")
    print("   • README.md - Complete documentation")
    print("   • config.yaml - System configuration")
    print("   • logs/ - Log files")
    
    print("\n🔧 Configuration:")
    print("   • Edit config.yaml to customize the system")
    print("   • Add .txt files to the Archive/ directory")
    
    print("\n📞 Support:")
    print("   • Check logs/application.log for errors")
    print("   • Consult README.md for documentation")
    
    print("\n🐍 Virtual Environment:")
    print("   • All dependencies are installed in the 'venv' directory")
    print("   • Activate with: source venv/bin/activate (Linux/Mac)")
    print("   • Activate with: venv\\Scripts\\activate (Windows)")
    
    print("\n" + "="*60)


def main():
    """Main installation function"""
    print_banner()
    
    # Pre-installation checks
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    # Installation steps
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    if not check_data_directory():
        print("❌ Failed to verify data directory")
        sys.exit(1)
    
    if not run_tests():
        print("⚠️  Some tests failed, but installation can continue")
    
    if not create_startup_script():
        print("⚠️  Could not create startup script")
    
    # Final instructions
    show_usage_instructions()


if __name__ == "__main__":
    main() 