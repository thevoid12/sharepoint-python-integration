import logging
from config.config_loader import Config


AppConfig = Config.load_config()
def initiate_logger():
    try:
        logging.basicConfig( format="{asctime} - {levelname} - {message}",
                    style="{",
                    datefmt="%Y-%m-%d %H:%M",
                    filename=AppConfig["app"]["logfilepath"],
                    encoding="utf-8",
                    filemode="a",
                    level=logging.DEBUG  
                    )
        logging.info("this is a test info")
    except Exception as e:
        logging.error("Error occurred: %s", e)
        raise
