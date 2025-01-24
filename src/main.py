"""Main module for the project.

This is the entry point for the project.
"""

from helpers.config import PROJECT_NAME, VERSION, PLOTS_DIR


def main():
    """The main function of the project."""
    print(f"Starting {PROJECT_NAME} version {VERSION}")
    print("Hello, World!")
    print(f"Plots directory: {PLOTS_DIR}")


if __name__ == "__main__":
    main()
