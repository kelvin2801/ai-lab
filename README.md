# ai-lab

## Environment Checking Script

This repository contains an environment checking script located at `scripts/check_env.py`.

### Goal
To verify that the local environment has the necessary dependencies installed to run the AI lab infrastructure and scripts effectively.

### Scope
The script accepts dependencies as command-line arguments and checks for their availability using the system path. It writes the results to a log file (`env_check.log`) for later review, ensuring that missing dependencies can be clearly identified.
