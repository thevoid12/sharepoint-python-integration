"""
auth.py

This module contains functions designed to handle authentication
and sign-in processes for SharePoint accounts.
These functions ensure secure access by verifying the certificate 
file and facilitating the login procedure
into the SharePoint environment.

Usage:
    - Import the necessary functions from this module in any part 
    of the application where authentication
      and sign-in processes for SharePoint are required.
    - The authentication functions handle certificate verification 
    and session management to provide
      secure access to SharePoint resources.

"""

import logging
from typing import Dict, Any
from office365.sharepoint.client_context import ClientContext
from config.config_loader import Config

AppConfig: Dict[str, Any] = Config.load_config()


def auth():
    """
    auth
    This function will authenticate the user using the certificate
    and return the SharePoint client context object.
    """
    client_id = AppConfig["sharepointauth"]["clientID"]
    thumbprint = AppConfig["sharepointauth"]["thumbPrint"]
    cert_path = AppConfig["sharepointauth"]["certificatePath"]
    site_url = AppConfig["sharepointauth"]["siteUrl"]
    try:
        cert_settings = {
            "client_id": client_id,
            "thumbprint": thumbprint,
            "cert_path": cert_path,
        }
        ctx = ClientContext(site_url).with_client_certificate(
            "auditcuetechnologies.onmicrosoft.com", **cert_settings
        )
        current_web = ctx.web
        ctx.load(current_web)
        ctx.execute_query()
        return ctx

    except Exception as e:
        logging.error("Error occurred: %s", e)
        raise
