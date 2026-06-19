import logging
import shutil
import sys
import os
import re

def setup_logger(log_file="env_check.log"):
    """Set up the logger to write to a file."""
    logger = logging.getLogger("EnvCheckLogger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger

def parse_agents_md_for_dependencies(filepath, logger):
    """Parse AGENTS.md to dynamically identify implied dependencies."""
    dependencies = set()

    if not os.path.exists(filepath):
        logger.warning(f"{filepath} not found. Cannot determine dependencies.")
        return list(dependencies)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()

            # Dynamically infer dependencies based on keywords in AGENTS.md
            if 'infrastructure-as-code' in content or 'iac' in content:
                logger.info("Found IaC references in AGENTS.md. Adding 'terraform' to dependencies.")
                dependencies.add('terraform')

            if 'local llm' in content:
                logger.info("Found Local LLM references in AGENTS.md. Adding 'ollama' to dependencies.")
                dependencies.add('ollama')

            if 'pull request' in content or 'repository' in content:
                logger.info("Found repository/PR references in AGENTS.md. Adding 'git' to dependencies.")
                dependencies.add('git')

            if 'python' in content:
                logger.info("Found Python references in AGENTS.md. Adding 'python3' and 'pip' to dependencies.")
                dependencies.add('python3')
                dependencies.add('pip')

            if 'docker' in content or 'container' in content:
                logger.info("Found container references in AGENTS.md. Adding 'docker' to dependencies.")
                dependencies.add('docker')

            if '.env' in content or 'environment variables' in content:
                 # Standard utility that might be needed, but maybe not a binary
                 pass

    except Exception as e:
        logger.error(f"Failed to parse {filepath}: {e}")

    return list(dependencies)

def check_dependencies(dependencies, logger):
    """Check if the list of dependencies is available in the system PATH."""
    all_present = True
    for dep in dependencies:
        try:
            path = shutil.which(dep)
            if path:
                logger.info(f"Dependency '{dep}' found at: {path}")
            else:
                logger.error(f"Dependency '{dep}' not found in system PATH.")
                all_present = False
        except Exception as e:
            logger.error(f"Error checking dependency '{dep}': {e}")
            all_present = False

    return all_present

def main():
    logger = setup_logger('env_check.log')
    logger.info("Starting environment dependency check...")

    # Path to AGENTS.md, assuming script is run from project root or scripts/ dir
    # Try multiple common locations
    agents_md_path = 'AGENTS.md'
    if not os.path.exists(agents_md_path):
        agents_md_path = '../AGENTS.md'

    dependencies = parse_agents_md_for_dependencies(agents_md_path, logger)

    if not dependencies:
        logger.warning("No dependencies identified from AGENTS.md.")
        sys.exit(0)

    success = check_dependencies(dependencies, logger)

    if success:
        logger.info("Environment check completed successfully. All dependencies are present.")
        sys.exit(0)
    else:
        logger.error("Environment check failed. Some dependencies are missing.")
        sys.exit(1)

if __name__ == "__main__":
    main()
