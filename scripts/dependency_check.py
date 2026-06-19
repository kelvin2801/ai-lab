import importlib.metadata
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# List of required Python packages to check
REQUIRED_PACKAGES = [
    # Example: "requests", "flask", "boto3"
    "requests",
]

def check_dependencies():
    """
    Checks if the required Python packages are installed.
    Logs missing packages and returns a list of them.
    """
    missing_packages = []
    installed_packages = {}

    for package in REQUIRED_PACKAGES:
        try:
            version = importlib.metadata.version(package)
            installed_packages[package] = version
            logging.info(f"Package '{package}' is installed (version: {version}).")
        except importlib.metadata.PackageNotFoundError:
            missing_packages.append(package)
            logging.warning(f"Package '{package}' is MISSING.")

    if missing_packages:
        logging.error(f"Missing packages detected: {', '.join(missing_packages)}")
    else:
        logging.info("All required packages are installed.")

    return missing_packages

if __name__ == "__main__":
    logging.info("Starting dependency check...")
    missing = check_dependencies()
    if missing:
        sys.exit(1)
    else:
        sys.exit(0)
