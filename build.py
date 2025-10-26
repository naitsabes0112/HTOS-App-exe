import subprocess
import shutil
import os
import sys

# --- Configuration ---
APP_SCRIPT = "app.py"
APP_NAME_CONSOLE = "HTOSApp"
APP_NAME_NOCMD = "HTOSAppNoCMD"

# Output paths for the builds
DIST_CONSOLE_PATH = "./dist_app"
DIST_NOCMD_PATH = "./dist_nocmd"
BUILD_CONSOLE_PATH = "./build_app"
BUILD_NOCMD_PATH = "./build_nocmd"

# Automatically uses the correct path separator (';' for Windows, ':' for Linux/Mac)
separator = ";" if sys.platform == "win32" else ":"

# --- Base PyInstaller Arguments (Common to both builds) ---
BASE_ARGS = [
    "pyinstaller",
    "--onefile",
    "--noconfirm",
    f"--add-data=data{separator}data",
    f"--add-data=google_drive{separator}google_drive",
    "--copy-metadata=aioftp",
    "--collect-data=nicegui",
    "--collect-submodules=nicegui",
]

# --- .env File Content ---
# This content will be written to a .env file in the output directories
ENV_FILE_CONTENT = """IP =
FTP_PORT = 2121
CECIE_PORT = 1234
UPLOAD_PATH =
MOUNT_PATH =
GOOGLE_DRIVE_JSON_PATH =
STORED_SAVES_FOLDER_PATH = STORAGE
TOKEN =
NPSSO =
"""

def clean_build_folders():
    """Cleans up old build and dist directories."""
    print("Cleaning up old build directories...")
    folders_to_clean = [
        DIST_CONSOLE_PATH, DIST_NOCMD_PATH,
        BUILD_CONSOLE_PATH, BUILD_NOCMD_PATH
    ]
    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"Removed directory: {folder}")
            except OSError as e:
                print(f"Error while deleting {folder}: {e}")
    print("Cleanup complete.\n")

def create_env_file(output_directory):
    """Creates a default .env file in the specified directory."""
    env_path = os.path.join(output_directory, ".env")
    print(f"Creating .env file at: {env_path}")
    try:
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(ENV_FILE_CONTENT)
        print(".env file created successfully.\n")
    except OSError as e:
        print(f"!!! ERROR: Failed to create .env file: {e}\n")

def run_build(command):
    """Executes a single PyInstaller command."""
    try:
        # Show the command being executed
        print(f"Executing: {' '.join(command)}")
        # Run the command
        subprocess.run(command, check=True)
        print("Build successful.\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"!!! ERROR: Build failed.")
        print(f"Return code: {e.returncode}")
        return False
    except FileNotFoundError:
        print("!!! ERROR: 'pyinstaller' not found.")
        print("Please ensure PyInstaller is installed (pip install pyinstaller)")
        return False


def main():
    # 1. Clean up old folders
    clean_build_folders()

    # 2. Build command for HTOSApp (with Console)
    print("=== Starting Build: HTOSApp (with Console) ===")

    cmd_console = BASE_ARGS + [
        f"--name={APP_NAME_CONSOLE}",
        f"--distpath={DIST_CONSOLE_PATH}",
        f"--workpath={BUILD_CONSOLE_PATH}",
        APP_SCRIPT,
    ]

    # Run the console build and exit if it fails
    if not run_build(cmd_console):
        print("Stopping build process due to error.")
        sys.exit(1)  # Exit script with an error code

    # Create the .env file for the console build
    create_env_file(DIST_CONSOLE_PATH)

    # 3. Build command for HTOSAppNoCMD (Windowed)
    print("=== Starting Build: HTOSAppNoCMD (Windowed) ===")

    cmd_nocmd = BASE_ARGS + [
        "--windowed",  # <-- Der einzige Unterschied
        f"--name={APP_NAME_NOCMD}",
        f"--distpath={DIST_NOCMD_PATH}",
        f"--workpath={BUILD_NOCMD_PATH}",
        APP_SCRIPT,
    ]

    # Run the windowed build
    if not run_build(cmd_nocmd):
        print("Stopping build process due to error.")
        sys.exit(1)

    # Create the .env file for the NoCMD build
    create_env_file(DIST_NOCMD_PATH)

    print("All builds completed successfully.")
    print(f"App (Console) in: {DIST_CONSOLE_PATH}")
    print(f"App (No CMD) in:  {DIST_NOCMD_PATH}")


if __name__ == "__main__":
    main()
