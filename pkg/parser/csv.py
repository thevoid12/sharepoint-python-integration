"""
csv.py
This file contains functions for parsing CSV files.
These functions includes logics to indetifity abnormality in the CSV 
files based on the csv type. 
"""

import os
import csv
import pandas as pd
from pkg.db.csv_type import CSVType
from pkg.db.db import FileManager
from config.config_loader import Config
from pkg.db.progressEnum import ProgressEnum
from pkg.hashing.hash import make_hash

AppConfig = Config.load_config()
def detect_abnormality(
    path,
    filename,
    csv_type=None
):
    """
    detect_abnormality
    This function will detect any abnormalities in the CSV file based on the CSV type.
    Args:
        file_path: The path to the CSV file.
        csv_type: The type of the CSV file.
    """
    if csv_type is None:
        fm = FileManager()
        csv_type = fm.read_file_record_by_path_and_filename(path, filename).csv_type

    try:
        print(f"Detecting abnormalities in ...")
        if csv_type == CSVType.PAYROLL:
            # Perform payroll specific checks
            print("Performing payroll specific checks...")
            _check_payroll(path, filename)
        elif csv_type == CSVType.VENDOR:
            # Perform vendor specific checks
            print("Performing vendor specific checks...")
            _check_vendor(path, filename)
        elif csv_type == CSVType.PO:
            # Perform PO specific checks
            print("Performing PO specific checks...")
            _check_PO(path, filename)
        elif csv_type == CSVType.INVOICE:
            # Perform invoice specific checks
            print("Performing invoice specific checks...")
            _check_invoice(path, filename)
        else:
            print("Unknown CSV type. Skipping abnormality detection.")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    return True


def _check_PO(path, filename):
    """
    _check_PO
    This function will check the PO CSV file for any abnormalities.
    Args:
        file_path: The path to the CSV file.
    """
    # fm = FileManager()
    final_path=f"{AppConfig["app"]["downloadDirectory"]}{path}/{filename}"
    final_save_path=f"{AppConfig["app"]["downloadDirectory"]}/out/{path}/{filename}"
    try:
        print("finalpath",final_path)
        if os.path.exists(final_path):
            print("The file exists.")
        else:
            print("The file does not exist.")
        data=pd.read_csv(final_path,skip_blank_lines=True)

        # Convert the relevant date columns to datetime
        data['Created On'] = pd.to_datetime(data['Created On'], format='%d/%m/%Y %I:%M %p')
        data['Business Approved On'] = pd.to_datetime(data['Business Approved On'])
        data['Finance Approved On'] = pd.to_datetime(data['Finance Approved On'])
        data['Treasury Approved On'] = pd.to_datetime(data['Treasury Approved On'])

        # Calculate the time differences
        data['Business Approval Delay'] = (data['Business Approved On'] - data['Created On']).dt.days
        data['Finance Approval Delay'] = (data['Finance Approved On'] - data['Created On']).dt.days
        data['Treasury Approval Delay'] = (data['Treasury Approved On'] - data['Created On']).dt.days

        # Find the rows where Business Approval is not T+3 and Finance Approval is not T+5
        not_satisfied = data[
        (data['Business Approval Delay'] > 3) |
        (data['Finance Approval Delay'] > 5) |
        (data['Treasury Approval Delay'] > 6)
        ]
        if not not_satisfied.empty:
            print("Rows where any approval delay does not meet the specified criteria:")
            print(not_satisfied[['Vendor ID', 'Vendor Name', 'Created On', 'Business Approved On', 'Business Approval Delay', 'Finance Approved On', 'Finance Approval Delay', 'Treasury Approved On', 'Treasury Approval Delay']])
        else:
            print("All approval delays meet the specified criteria.")
        os.makedirs(os.path.dirname(final_save_path), exist_ok=True)
        not_satisfied.to_csv(final_save_path, index=True)
        fm = FileManager()
        existing_file = fm.read_file_record_by_path_and_filename(f"/out{path}", filename)
        if existing_file:
            fm.update_file_record_from_path_name(
                path=path,
                filename=f"/out{path}",
                csv_type=CSVType.OUTPUT,
                sha256=make_hash(open(final_save_path, "rb").read()),
                progress=ProgressEnum.PARSED,
            )
        else:
            fm.create_file_record(
                filename=filename,
                path=f"/out{path}",
                filetype="csv",
                csv_type=CSVType.OUTPUT,
                sha256=make_hash(open(final_save_path, "rb").read()),
                progress=ProgressEnum.PARSED,
            )

    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    return True

def _check_invoice(path, filename):
    """
    _check_invoice
    This function will check the Invoice CSV file for any abnormalities.
    Args:
        file_path: The path to the CSV file.
    """
    # fm = FileManager()
    final_path=f"{AppConfig["app"]["downloadDirectory"]}{path}/{filename}"
    final_save_path=f"{AppConfig["app"]["downloadDirectory"]}/out/{path}/{filename}"
    try:
        print("finalpath",final_path)
        if os.path.exists(final_path):
            print("The file exists.")
        else:
            print("The file does not exist.")
        data=pd.read_csv(final_path,skip_blank_lines=True)
        print(data.keys())

        # Convert the relevant date columns to datetime
        data['Created On'] = pd.to_datetime(data['Created On'], format='%d/%m/%Y %I:%M %p')
        data['Business Approved On'] = pd.to_datetime(data['Business Approved on'])
        data['Finance Approved On'] = pd.to_datetime(data['Finance Approved on'])

        # Calculate the time differences
        data['Business Approval Delay'] = (data['Business Approved On'] - data['Created On']).dt.days
        data['Finance Approval Delay'] = (data['Finance Approved On'] - data['Created On']).dt.days

        # Find the rows where Business Approval is not T+3 and Finance Approval is not T+5
        not_satisfied = data[
        (data['Business Approval Delay'] > 3) |
        (data['Finance Approval Delay'] > 5) 
        ]
        if not not_satisfied.empty:
            print("Rows where any approval delay does not meet the specified criteria:")
            print(not_satisfied[['Vendor ID', 'Vendor Name', 'Created On', 'Business Approved on', 'Business Approval Delay', 'Finance Approved on', 'Finance Approval Delay']])
        else:
            print("All approval delays meet the specified criteria.")
        os.makedirs(os.path.dirname(final_save_path), exist_ok=True)
        not_satisfied.to_csv(final_save_path, index=True)
        fm = FileManager()
        existing_file = fm.read_file_record_by_path_and_filename(f"/out{path}", filename)
        if existing_file:
            fm.update_file_record_from_path_name(
                path=f"/out{path}",
                filename=filename,
                csv_type=CSVType.OUTPUT,
                sha256=make_hash(open(final_save_path, "rb").read()),
                progress=ProgressEnum.PARSED,
            )
        else:
            fm.create_file_record(
                filename=filename,
                path=f"/out{path}",
                filetype="csv",
                csv_type=CSVType.OUTPUT,
                sha256=make_hash(open(final_save_path, "rb").read()),
                progress=ProgressEnum.PARSED,
            )
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    return True

def _check_vendor(path, filename):
    """
    _check_vendor
    This function will check the Vendor CSV file for any abnormalities.
    Args:
        file_path: The path to the CSV file.
    """
    # fm = FileManager()
    final_path=f"{AppConfig["app"]["downloadDirectory"]}{path}/{filename}"
    final_save_path=f"{AppConfig["app"]["downloadDirectory"]}/out/{path}/{filename}"
    try:
        print("finalpath",final_path)
        if os.path.exists(final_path):
            print("The file exists.")
        else:
            print("The file does not exist.")
        data=pd.read_csv(final_path,skip_blank_lines=True)
        # Drop unnecessary rows and colums that have only NaN values
        data = data.dropna(how='all')
        data = data.dropna(axis=1, how='all')
        # Rename the columns for easier access
        data.columns = ['S_No', 'Documents', 'Comments', 'Status']

        # Drop rows with blank S.No
        data = data.dropna(subset=['S_No'])

        # Reset the index
        data.reset_index(drop=True, inplace=True)

        # Find the rows where Status is not "Validated"
        not_validated_rows = data[data['Status'] != 'Validated']

        print("Rows that are not Validated:")
        print(not_validated_rows) 
        os.makedirs(os.path.dirname(final_save_path), exist_ok=True)
        not_validated_rows.to_csv(final_save_path, index=True)
        fm = FileManager()
        existing_file = fm.read_file_record_by_path_and_filename(f"/out{path}", filename)
        if existing_file:
            fm.update_file_record_from_path_name(
                path=f"/out{path}",
                filename=filename,
                csv_type=CSVType.OUTPUT,
                sha256=make_hash(open(final_save_path, "rb").read()),
                progress=ProgressEnum.PARSED,
            )
        else:
            fm.create_file_record(
                filename=filename,
                path=f"/out{path}",
                filetype="csv",
                csv_type=CSVType.OUTPUT,
                sha256=make_hash(open(final_save_path, "rb").read()),
                progress=ProgressEnum.PARSED,
            )
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    return True

def _check_payroll(path, filename):
    """
    _check_payroll
    This function will check the Payroll CSV file for any abnormalities.
    Args:
        file_path: The path to the CSV file.
    """
    # fm = FileManager()
    final_path=f"{AppConfig["app"]["downloadDirectory"]}{path}/{filename}"
    final_save_path=f"{AppConfig["app"]["downloadDirectory"]}/out/{path}/{filename}"
    try:
        print("finalpath",final_path)
        if os.path.exists(final_path):
            print("The file exists.")
        else:
            print("The file does not exist.")
        
        data = pd.read_csv(final_path, skiprows=5)
        print(data.head())

        # Rename the columns for easier access
        data.columns = ['Emp_ID_HR', 'Loss_of_Pay_HR', 'Empty_Column', 'Emp_ID_Payroll', 'Loss_of_Pay_Payroll']

        # Drop the unnecessary columns
        data = data.drop(columns=['Empty_Column'])

        # Find the rows where Loss of Pay doesn't tally
        mismatch_rows = data[(data['Loss_of_Pay_HR'] != data['Loss_of_Pay_Payroll']) & (~data['Loss_of_Pay_HR'].isna())]

        print("Rows where Loss of Pay doesn't tally:")
        print(mismatch_rows)
        os.makedirs(os.path.dirname(final_save_path), exist_ok=True)
        mismatch_rows.to_csv(final_save_path, index=True)
        fm = FileManager()
        existing_file = fm.read_file_record_by_path_and_filename(f"/out{path}", filename)
        if existing_file:
            fm.update_file_record_from_path_name(
                path=f"/out{path}",
                filename=filename,
                csv_type=CSVType.OUTPUT,
                sha256=make_hash(open(final_save_path, "rb").read()),
                progress=ProgressEnum.PARSED,
            )
        else:
            fm.create_file_record(
                filename=filename,
                path=f"/out{path}",
                filetype="csv",
                csv_type=CSVType.OUTPUT,
                sha256=make_hash(open(final_save_path, "rb").read()),
                progress=ProgressEnum.PARSED,
            )
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    return True


def test():
    fm = FileManager()
    all_csv_files = fm.read_all_files_by_filetype("csv")
    print("All csv",all_csv_files)
    for i in all_csv_files:
        if i.csv_type is None:
            continue
        if i.csv_type == CSVType.OUTPUT:
            continue
        detect_abnormality(i.path, i.filename,i.csv_type)
