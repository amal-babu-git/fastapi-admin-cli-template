#!/usr/bin/env python
"""
Management script for FastAPI projects.
This script is a wrapper for the fastapi-admin-cli package commands.
"""
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run administrative tasks."""
    # Add the project root to the Python path
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    
    try:
        # Import the CLI functionality from fastapi-admin-cli
        from fastapi_admin.cli import run_from_command_line
        
        # Pass all command line arguments to the fastapi-admin CLI
        run_from_command_line()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import fastapi-admin-cli. Make sure it's installed and "
            "available on your PYTHONPATH environment variable. You might need "
            "to run 'pip install fastapi-admin-cli'."
        ) from exc

if __name__ == "__main__":
    main()
