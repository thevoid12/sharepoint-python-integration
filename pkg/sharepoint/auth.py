"""
auth.py

This module contains functions designed to handle authentication and sign-in processes for SharePoint accounts.
These functions ensure secure access by verifying the certificate file and facilitating the login procedure
into the SharePoint environment.

Usage:
    - Import the necessary functions from this module in any part of the application where authentication
      and sign-in processes for SharePoint are required.
    - The authentication functions handle certificate verification and session management to provide
      secure access to SharePoint resources.

"""

import requests
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.runtime.auth.user_credential import UserCredential
from config.config_loader import appconfig
from msal import ConfidentialClientApplication
import logging


def auth():
    client_id = appconfig['sharepointauth']['clientID']
    thumbprint = appconfig['sharepointauth']['thumbPrint']
    cert_path = appconfig['sharepointauth']['certificatePath']
    site_url = appconfig['sharepointauth']['siteUrl']
    try:
        cert_settings = {
        'client_id': client_id, 
        'thumbprint': thumbprint,
        'cert_path': cert_path
          }
        ctx = ClientContext(site_url).with_client_certificate('auditcuetechnologies.onmicrosoft.com', **cert_settings)
        current_web = ctx.web
        ctx.load(current_web)
        ctx.execute_query()
        return ctx

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise
