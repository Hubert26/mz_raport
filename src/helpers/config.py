"""Project configuration settings.

This module contains basic configuration settings for the project,
including environment variables.
"""

from dotenv import dotenv_values
from pathlib import Path

# Project-specific settings
PROJECT_NAME = "mz_raport"
VERSION = "0.1.0"
AUTHOR = "Hubert Szewczyk"

# Load environment variables from the .env file
env_vars = dotenv_values()  # Load variables from the .env file

# Get the workspace path from the environment variables
WORKSPACE_PATH = Path(env_vars.get("WORKSPACE_PATH"))  # Fetch WORKSPACE_PATH from .env

if not WORKSPACE_PATH:
    raise ValueError("WORKSPACE_PATH is not defined in the .env file or is empty.")

DATA_DIR = Path(env_vars["DATA_DIR"])
RESULTS_DIR = Path(env_vars["RESULTS_DIR"])
PLOTS_DIR = Path(env_vars["PLOTS_DIR"])
