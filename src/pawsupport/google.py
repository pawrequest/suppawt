from __future__ import print_function
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dataclasses import dataclass
from typing import Dict, List, Optional




SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY_MAP_SHEET_ID = r'1UtePMfdr-svthUGhUnWBIVRz_SgIB8z9ppOG7t_iGc0'
KEY_MAP_RANGE_NAME = 'Sheet1'



def main():
    ...


def get_sheets_values():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    token = 'user_data/token.json'
    if os.path.exists(token):
        creds = Credentials.from_authorized_user_file(token, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'user_data/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('user_data/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=KEY_MAP_SHEET_ID,
                                    range=KEY_MAP_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        return values

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
