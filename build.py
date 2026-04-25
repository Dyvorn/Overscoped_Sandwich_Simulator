import subprocess
import shutil
import os
import sys

GAME_SCRIPT_NAME = "OVER-SCOPED SANDWICH SIMULATOR.py"
APP_NAME = "Overscoped Sandwich Simulator"

def install_dependencies():
    """Installs necessary Python packages."""
    print("Installing/upgrading dependencies (this might take a moment)...") #
    packages = ["pyinstaller", "PyQt6", "PyQt6-Qt6"]
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
            print(f"Successfully installed/upgraded {package}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            sys.exit(1)

def build_executable():
    """Builds the executable using PyInstaller."""
    print(f"Building {APP_NAME} executable with PyInstaller...")
    
    # Clean up previous build artifacts
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    command = [
        "pyinstaller",
        "--noconfirm",      # Don't ask for confirmation
        "--onefile",        # Create a single executable file
        "--windowed",       # No console window
        f"--name={APP_NAME}", # Name of the executable
        f"--add-data=sounds;sounds", # Add sounds folder
        f"--add-data=images;images", # Add images folder
        GAME_SCRIPT_NAME
    ]
    
    try:
        subprocess.check_call(command)
        print(f"Successfully built {APP_NAME} executable in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"Error during PyInstaller build: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_dependencies()
    build_executable()