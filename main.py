"""
main.py

main.py serves as the entry point for the application. It initializes
the application, loads the necessary configuration settings, and starts
the main processes or functions defined within the application.

Usage:
    Execute this script to run the application. The configuration settings
    are loaded from the config_loader module to ensure consistent and centralized
    access to configuration data across the entire application.

"""

import pkg.sharepoint.auth as spauth


def main():
    """
    main
    The main function of the application that initializes the application
    and starts the main processes or functions.

    """
    spauth.auth()
    return


if __name__ == "__main__":
    main()
