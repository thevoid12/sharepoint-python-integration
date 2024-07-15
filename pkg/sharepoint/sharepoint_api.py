from config.config_loader import appconfig
from office365.sharepoint.files.file import File
import os


def list_all_folders(ctx):
    relative_url = appconfig["sharepointauth"]["docRelativeUrl"]
    root_folder = ctx.web.get_folder_by_server_relative_url(relative_url)
    root_folder.expand(["Files", "Folders"]).get().execute_query()
    for files in root_folder.files:
        print(files)


def list_all_files(ctx):
    relative_url = appconfig["sharepointauth"]["docRelativeUrl"]
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
    return files


def save_file(ctx, file):
    parent_dir = file.parent_collection.parent.serverRelativeUrl
    file_n = file.name
    file_obj = File.open_binary(ctx, file.serverRelativeUrl).content
    file_dir_path = appconfig["app"]["downloadDirectory"] + parent_dir + "/" + file_n
    os.makedirs(os.path.dirname(file_dir_path), exist_ok=True)
    with open(file_dir_path, "wb") as f:
        f.write(file_obj)
    return


def download_all_files(ctx, files):
    for file in files:
        save_file(ctx, file)
    return
