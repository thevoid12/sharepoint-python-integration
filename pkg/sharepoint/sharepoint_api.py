from config.config_loader import appconfig

def list_all_folders(ctx):
      relative_url = appconfig['sharepointauth']['docRelativeUrl']
      root_folder = ctx.web.get_folder_by_server_relative_url(relative_url)
      root_folder.expand(["Files", "Folders"]).get().execute_query()
      for files in root_folder.files:
       print(files)
