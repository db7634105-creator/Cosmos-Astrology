"""
YouTube Channel Video Viewer - Installation Helper
Run this script to set up all dependencies
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50 + "\n")


def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    version_info = sys.version_info
    version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    print(f"✓ Python {version_str} detected")
    
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 7):
        print("✗ Python 3.7+ is required")
        print("  Download from: https://www.python.org")
        return False
    return True


def check_pip():
    """Check if pip is available"""
    print_header("Checking pip")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        print(f"✓ {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"✗ pip not found: {e}")
        return False


def install_requirements():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    requirements = [
        "pillow>=9.0.0",
        "requests>=2.28.0",
        "yt-dlp>=2023.0.0",
        "beautifulsoup4>=4.11.0"
    ]
    
    for package in requirements:
        print(f"Installing {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", package],
                         check=True, capture_output=True)
            print(f"✓ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}")
            print(f"  Error: {e}")
            return False
    
    return True


def verify_installation():
    """Verify all packages are installed"""
    print_header("Verifying Installation")
    
    packages = {
        'PIL': 'Pillow',
        'requests': 'requests',
        'yt_dlp': 'yt-dlp',
        'bs4': 'BeautifulSoup4'
    }
    
    all_installed = True
    for import_name, display_name in packages.items():
        try:
            __import__(import_name)
            print(f"✓ {display_name} is installed")
        except ImportError:
            print(f"✗ {display_name} is NOT installed")
            all_installed = False
    
    return all_installed


def check_script_files():
    """Check if script files exist"""
    print_header("Checking Script Files")
    
    scripts = [
        "youtube_channel_viewer.py",
        "youtube_channel_viewer_api.py",
        "run_viewer.bat",
        "run_viewer_api.bat"
    ]
    
    script_dir = Path(__file__).parent
    all_exist = True
    
    for script in scripts:
        script_path = script_dir / script
        if script_path.exists():
            print(f"✓ {script} found")
        else:
            print(f"✗ {script} NOT found")
            all_exist = False
    
    return all_exist


def show_next_steps():
    """Show next steps"""
    print_header("Setup Complete!")
    print("""
Next Steps:

1. Using Batch Files (Easiest):
   - Double-click 'run_viewer.bat' to start the application
   - Or double-click 'run_viewer_api.bat' for API version

2. Using PowerShell:
   cd "C:\\Users\\dines\\OneDrive\\Documents\\Blogs"
   python youtube_channel_viewer.py

3. For API Version:
   python youtube_channel_viewer_api.py

Features:
  ✓ Displays all videos from your channel
  ✓ Click thumbnail to watch on YouTube
  ✓ Pagination for easy browsing
  ✓ Auto-updates when new videos uploaded
  ✓ No API key required (for Version 1)

Troubleshooting:
  - If videos don't load, try upgrading yt-dlp:
    pip install --upgrade yt-dlp
  
  - For API version, get free API key from:
    https://console.cloud.google.com/

Questions? Check the guides:
  - QUICK_START.md (5-minute setup)
  - SETUP_GUIDE.md (detailed instructions)

Happy watching! 🎬
""")


def main():
    """Main installation flow"""
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " YouTube Channel Video Viewer Setup ".center(48) + "║")
    print("╚" + "=" * 48 + "╝")
    
    # Step 1: Check Python
    if not check_python_version():
        return False
    
    # Step 2: Check pip
    if not check_pip():
        return False
    
    # Step 3: Install requirements
    if not install_requirements():
        print("\n⚠ Some packages failed to install")
        print("Try running in PowerShell:")
        print("pip install -r requirements.txt")
        return False
    
    # Step 4: Verify
    if not verify_installation():
        print("\n⚠ Some packages could not be verified")
        return False
    
    # Step 5: Check scripts
    check_script_files()
    
    # Step 6: Show next steps
    show_next_steps()
    
    return True


if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n⚠ Setup encountered issues. Please check the error messages above.")
        print("You can also:")
        print("1. Visit: https://www.python.org")
        print("2. Run: pip install -r requirements.txt")
        input("\nPress Enter to exit...")
    else:
        input("\n✓ Setup completed successfully! Press Enter to exit...")
