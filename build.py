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
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Deleted old {folder} folder.")

    command = [
        "pyinstaller",
        "--noconfirm",      # Don't ask for confirmation
        "--onefile",        # Create a single executable file
        "--windowed",       # No console window
        "--clean",          # Clean PyInstaller cache
        f"--name={APP_NAME}", # Name of the executable
        GAME_SCRIPT_NAME
    ]

    # Dynamically add data folders if they exist
    for folder in ["sounds", "images"]:
        if os.path.exists(folder):
            command.insert(5, f"--add-data={folder}{os.pathsep}{folder}")

    try:
        subprocess.check_call(command)
        print(f"Successfully built {APP_NAME} executable in the 'dist' folder.")
        # Final cleanup of the spec file
        spec_file = f"{APP_NAME}.spec"
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"Removed {spec_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during PyInstaller build: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_dependencies()
    build_executable()