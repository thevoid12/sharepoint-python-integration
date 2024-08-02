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

from pkg.db.db import FileManager
from pkg.db.csv_type import CSVType
import pkg.sharepoint.auth as spauth
import pkg.sharepoint.sharepoint_api as spapi
from pkg.parser.csv import detect_abnormality
from pkg.parser.xlsx import convert_to_csv, find_csv_type
from logger import logger as log
import logging
import time


def main():
    """
    main
    The main function of the application that initializes the application
    and starts the main processes or functions.

    """
    log.initiate_logger()
    ctx = spauth.auth()
    all_files = spapi.list_all_files(ctx)
    spapi.download_all_files(ctx, all_files)
    logging.debug(spapi.get_changed_files(ctx, all_files))
    fm = FileManager()
    all_xlsx_files = fm.read_all_files_by_filetype("xlsx")
    logging.debug("All xlsx files:", all_xlsx_files)
    for i in all_xlsx_files:
        try:
            convert_to_csv(i.path, i.filename)
        except Exception as e:
            logging.error(
                f"Error occurred: {e} has occured while converting {i.path} {i.filename}."
            )
        logging.info(f"{i.path}\t{i.filename}\t{i.csv_type} has been converted.")
    all_csv_files = fm.read_all_files_by_filetype("csv")
    logging.debug(all_csv_files)
    for i in all_csv_files:
        find_csv_type(i.path, i.filename)
        logging.debug(f"{i.path}\t{i.filename}\t{i.csv_type}")
    new_fm = FileManager()
    new_csv = new_fm.read_all_files_by_filetype("csv")
    logging.debug(f"All {len(new_csv)}csv", new_csv)
    for i in new_csv:
        if i.csv_type is None:
            continue
        else:
            logging.info(i.path, i.filename, i.csv_type, "Detecting abnormalities...")
        if i.csv_type == CSVType.OUTPUT:
            continue

        detect_abnormality(i.path, i.filename, i.csv_type)
    logging.info(
        "Your files are parsed and checked for abnormalities. Check the output folder for the results."
    )
    logging.debug("this is a debug test log in main file")
    logging.error("this is a error test log in main file")
    spauth.teslog()

    return


if __name__ == "__main__":
    main()
