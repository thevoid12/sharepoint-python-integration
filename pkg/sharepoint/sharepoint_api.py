"""
sharepoint_api.py

This module contains functions designed to interact with SharePoint
to list, download, and save files from the SharePoint site.
These functions utilize the SharePoint client context object to
access and manipulate files and folders in the SharePoint environment.

Usage:
    - Import the necessary functions from this module in any part
    of the application where SharePoint file operations are required.
    - The functions in this module provide the ability to list all files
    and folders, download files, and save files to the local directory.

"""

import os
from typing import Dict, Any
from office365.sharepoint.files.file import File
from config.config_loader import Config
from pkg.hashing.hash import make_hash
from pkg.db.db import FileManager
from pkg.db.progressEnum import ProgressEnum
import logging

AppConfig: Dict[str, Any] = Config.load_config()


def list_all_folders(ctx):
    """
    list_all_folders
    This funtion will list all the folders in the SharePoint site primary Directory.
    Args:
        ctx: The SharePoint client context object.
    """
    relative_url = AppConfig["sharepointauth"]["docRelativeUrl"]
    root_folder = ctx.web.get_folder_by_server_relative_url(relative_url)
    root_folder.expand(["Files", "Folders"]).get().execute_query()
    for files in root_folder.files:
        logging.info(files)


def list_all_files(ctx):
    """
    list_all_files
    This funtion will list all the files in the SharePoint site. We crawl through the folder
    and subfolders to list all the files
    Args:
        ctx: The SharePoint client context object.
    """
    try:
        relative_url = AppConfig["sharepointauth"]["docRelativeUrl"]
        root_folder = ctx.web.get_folder_by_server_relative_url(relative_url)
        root_folder.expand(["Files", "Folders"]).get().execute_query()
        files = list(root_folder.files)
        folders = list(root_folder.folders)
        while len(folders) > 0:
            current_folder = folders.pop()
            current_folder.expand(["Files", "Folders"]).get().execute_query()
            files = files + list(current_folder.files)
            current_folder_folders = list(current_folder.folders)
            while len(current_folder_folders) > 0:
                folders.append(current_folder_folders.pop())
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise
    return files


def save_file(ctx, file):
    """
    save_file
    This funtion will save the file to the local directory.
    Args:
        ctx: The SharePoint client context object.
        file: The file object to be saved.
    """
    try:
        parent_dir = file.parent_collection.parent.serverRelativeUrl
        file_n = file.name
        file_obj = File.open_binary(ctx, file.serverRelativeUrl).content
        file_dir_path = (
            # os.path.join(AppConfig["app"]["downloadDirectory"], parent_dir, file_n)
            AppConfig["app"]["downloadDirectory"]
            + parent_dir
            + "/"
            + file_n
        )
        os.makedirs(os.path.dirname(file_dir_path), exist_ok=True)
        with open(file_dir_path, "wb") as f:
            f.write(file_obj)
        logging.info(f"File {file.serverRelativeUrl} saved successfully")
    except OSError as e:
        logging.error(
            f"OS Error occurred: This might be beacase there are permission issues {e}"
        )
        raise
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise
    return True


def download_all_files(ctx, files):
    """
    download_all_files
    This funtion will download all the files in the SharePoint site.
    Args:
        ctx: The SharePoint client context object.
        files: The list of file objects to be downloaded.
    """
    try:

        fileManager = FileManager()
        for file in files:
            save_file(ctx, file)
            current_hash = make_hash(
                File.open_binary(ctx, file.serverRelativeUrl).content
            )
            db_file = fileManager.read_file_record_by_path_and_filename(
                file.parent_collection.parent.serverRelativeUrl, file.name
            )
            if db_file is not None:
                db_hash = db_file.sha256
                if current_hash == db_hash:
                    logging.info(f"File {file.name} is unchanged downloaded")
                    continue
                else:
                    file_type = file.name.split(".")[-1]
                    fileManager.update_file_record(
                        fileManager.read_file_record_by_path_and_filename(
                            file.parent_collection.parent.serverRelativeUrl, file.name
                        ).id,
                        sha256=current_hash,
                        progress=ProgressEnum.DOWNLOADED,
                        filetype=file_type,
                    )
            else:
                file_type = file.name.split(".")[-1]
                fileManager.create_file_record(
                    file.parent_collection.parent.serverRelativeUrl,
                    file.name,
                    current_hash,
                    ProgressEnum.DOWNLOADED,
                    file_type,
                )

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise
    return True


def get_changed_files(ctx, files):
    """
    get_changed_files
    This funtion will get the list of files that have been changed in the SharePoint site.
    Args:
        ctx: The SharePoint client context object.
        files: The list of file objects to be checked for changes.
    """
    try:
        changed_files = []
        fileManager = FileManager()
        for file in files:
            save_file(ctx, file)
            current_hash = make_hash(
                File.open_binary(ctx, file.serverRelativeUrl).content
            )
            db_file = fileManager.read_file_record_by_path_and_filename(
                file.parent_collection.parent.serverRelativeUrl, file.name
            )
            if db_file is not None:
                db_hash = db_file.sha256
                if current_hash != db_hash:
                    changed_files.append(file)
                    file_type = file.name.split(".")[-1]
                    fileManager.update_file_record(
                        fileManager.read_file_record_by_path_and_filename(
                            file.parent_collection.parent.serverRelativeUrl, file.name
                        ).id,
                        sha256=current_hash,
                        progress=ProgressEnum.DOWNLOADED,
                        filetype=file_type,
                    )
            else:
                changed_files.append(file)
                file_type = file.name.split(".")[-1]
                fileManager.create_file_record(
                    file.parent_collection.parent.serverRelativeUrl,
                    file.name,
                    current_hash,
                    ProgressEnum.DOWNLOADED,
                    file_type,
                )
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise
    return changed_files
