"""
This file contains functions to handle Excel file operations such as reading
and covertiing it into a csv files for further processing. These functions can be used to read
Excel files, convert them to csv files, and extract data for analysis.
"""

import openpyxl
import os
from config.config_loader import Config
from pkg.db.db import FileManager
from pkg.db.progressEnum import ProgressEnum
from pkg.hashing.hash import make_hash
AppConfig = Config.load_config()


def read_file(path, file_name):
    """
    read_file
    This function will read from the given file path and file name.
    Args:
    path: The path to the file.
    file_name: The name of the file.
    """
    final_path = f"{AppConfig["app"]["downloadDirectory"]}/{path}/{file_name}"
    try:
        wb = openpyxl.load_workbook(final_path)
        sheet = wb.active
        for row in sheet.iter_rows():
            for cell in row:
                print(cell.value)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    return True

def convert_to_csv(path, file_name):
    """
    convert_to_csv
    This function will convert the given Excel file to a CSV file.
    Args:
    path: The path to the file.
    file_name: The name of the file.
    """
    final_path = f"{AppConfig["app"]["downloadDirectory"]}{path}{file_name}"
    os.makedirs(final_path.split('.')[0], exist_ok=True)
    try:
        wb = openpyxl.load_workbook(final_path)
        fm = FileManager()
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            # Construct a unique CSV file name for each sheet
            csv_file_path = f"{final_path.split('.')[0]}/{sheet_name}.csv"
            with open(csv_file_path, "w", encoding='utf-8') as csv_file:
                for row in sheet.iter_rows():
                    values = [str(cell.value) if cell.value is not None else '' for cell in row]
                    csv_file.write(",".join(values) + "\n")
                # print(f"CSV file {csv_file.read()} created successfully")
            with open(csv_file_path, "rb") as csv_file:
                current_hash = make_hash(csv_file.read())
            
            print(
                (path+file_name).split('.')[0],
                csv_file_path.split('/')[-1],
                current_hash,
                ProgressEnum.COMPLETED,
                "csv",
            )
            fm.create_file_record(
                filename=csv_file_path.split('/')[-1],
                path=(path+file_name).split('.')[0],
                sha256=current_hash,
                progress=ProgressEnum.COMPLETED,
                filetype="csv",
            )
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    return True


if __name__ == "__main__":
    read_file("/sites/NAF/Shared Documents/","Book.xlsx")
