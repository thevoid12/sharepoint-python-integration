"""
config_loader.py

This module is responsible for reading the configuration file (config.json)
and loading its contents into a dictionary. The loaded configuration is then
made available across the entire application for consistent and centralized
access to configuration settings.

Usage:
    - Import the config object from this module in any part of the application
      where configuration settings are required.
    - The configuration file is read only once, and the loaded configuration is
      cached for subsequent access to improve performance and ensure consistency.

"""

import json
from typing import Dict, Any


class Config:
    """
    Config
    This class is responsible for loading the configuration data from the
    specified JSON file and making it available for import across the application.
    """

    _config = None

    @classmethod
    def load_config(cls, config_file="./config/config.json") -> Dict[str, Any]:
        """
        Load the configuration from the specified JSON file.

        Args:
            config_file (str): The path to the configuration file. Default is 'config.json'.

        Returns:
            dict: The configuration data loaded from the JSON file.
        """
        if cls._config is None:
            with open(config_file, "r", encoding="utf-8") as file:
                cls._config = json.load(file)
        return cls._config


# Load the configuration once and make it available for import
appconfig: Dict[str, Any] = Config.load_config()
