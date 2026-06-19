import os
import logging
import shutil
import sys

# Configuration
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "dependency_check.log")

# Parameterized dependencies list
DEPENDENCIES = [
    "python3",
    "git",
    "docker",
    "pip"
]

def setup_logging():
    """Sets up logging for the script, ensuring the log directory exists."""
    if not os.path.exists(LOG_DIR):
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
        except OSError as e:
            print(f"Error creating log directory '{LOG_DIR}': {e}")
            sys.exit(1)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, mode='a'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependency(command):
    """Checks if a given dependency command is available in the system PATH."""
    try:
        # shutil.which returns the path to the executable or None
        if shutil.which(command):
            logging.info(f"SUCCESS: '{command}' is installed and found in PATH.")
            return True
        else:
            logging.error(f"MISSING: '{command}' is NOT installed or not in PATH.")
            return False
    except Exception as e:
        logging.error(f"ERROR: Failed to check for '{command}'. Exception: {e}")
        return False

def main():
    setup_logging()
    logging.info("Starting dependency check...")

    all_passed = True
    for dep in DEPENDENCIES:
        if not check_dependency(dep):
            all_passed = False

    if all_passed:
        logging.info("All dependencies are successfully installed.")
    else:
        logging.warning("One or more dependencies are missing. Please install them.")

if __name__ == "__main__":
    main()
