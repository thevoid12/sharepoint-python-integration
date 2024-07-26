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
import time


def main():
    """
    main
    The main function of the application that initializes the application
    and starts the main processes or functions.

    """
    ctx = spauth.auth()
    all_files = spapi.list_all_files(ctx)
    spapi.download_all_files(ctx, all_files)
    print(spapi.get_changed_files(ctx, all_files))
    fm = FileManager()
    all_xlsx_files = fm.read_all_files_by_filetype("xlsx")
    print("All xlsx files:", all_xlsx_files)
    for i in all_xlsx_files:
        convert_to_csv(i.path, i.filename)
        print(f"{i.path}\t{i.filename}\t{i.csv_type}")
    all_csv_files = fm.read_all_files_by_filetype("csv")
    print(all_csv_files)
    for i in all_csv_files:
        find_csv_type(i.path, i.filename)
        print(f"{i.path}\t{i.filename}\t{i.csv_type}")
    new_fm = FileManager()
    new_csv = new_fm.read_all_files_by_filetype("csv")
    print(f"All {len(new_csv)}csv", new_csv)
    for i in new_csv:
        print(i.path, i.filename, i.csv_type)
        if i.csv_type is None:
            continue
        if i.csv_type == CSVType.OUTPUT:
            continue
        detect_abnormality(i.path, i.filename, i.csv_type)
    print(
        "Your files are parsed and checked for abnormalities. Check the output folder for the results."
    )
    return


if __name__ == "__main__":
    main()
