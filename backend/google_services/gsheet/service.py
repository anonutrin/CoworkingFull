from typing import List, Optional

import gspread
from google.oauth2.service_account import Credentials
from .exceptions import *
from utils.logger import logger


class GoogleSheetService:

    def __init__(self, credentials_path: str, scopes: Optional[List] = None):
        self._key_path = credentials_path
        self._scopes = scopes if scopes else ['https://www.googleapis.com/auth/spreadsheets']
        self._creds = None
        self.client = None
        self.sheet = None

    def _load_credentials(self):
        try:
            self._creds = Credentials.from_service_account_file(self._key_path, scopes=self._scopes)
        except FileNotFoundError:
            logger.error('Unable to load credentials because the key path was not found')
        except Exception as e:
            logger.error(f'Error occurred while load credentials: {str(e)}')

    def _is_auth(self) -> bool:
        return bool(self.client)

    def authenticate(self):
        self._load_credentials()

        try:
            self.client = gspread.authorize(self._creds)
        except gspread.exceptions.GSpreadException as e:
            error_message = f"Authentication failed: {str(e)}"
            logger.error(error_message)
            raise GSheetAuthError(error_message)
        except Exception as e:
            error_message = f"Authentication error: {str(e)}"
            logger.error(error_message)
            raise GSheetAuthError(error_message)

    def load_sheet(self, sheet_url: str):
        if not self._is_auth():
            logger.error('Sheet cannot be loaded until client is authorized')
            return

        try:
            self.sheet = self.client.open_by_url(sheet_url)
        except gspread.exceptions.SpreadsheetNotFound as e:
            error_message = f'Sheet not found: {str(e)}'
            logger.error(error_message)
            raise GSheetLoadError(error_message)
        except gspread.exceptions.APIError as e:
            error_message = f'API Error: {str(e)}'
            logger.error(error_message)
            raise GSheetLoadError(error_message)
        except Exception as e:
            error_message = f'Error: {str(e)}'
            logger.error(error_message)
            raise GSheetLoadError(error_message)

    def is_closed(self) -> bool:
        return not self.sheet or not self._is_auth()

    def export_data_from_worksheet(self, worksheet_number: int = 0) -> List:
        if self.is_closed():
            logger.error(f'{self} - is not authorized and requires a worksheet to be loaded!')
            return []

        try:
            worksheet = self.sheet.get_worksheet(worksheet_number)
            return worksheet.get_all_values()

        except Exception as e:
            message_error = f'Error while export data from sheet: {str(e)}'
            logger.error(message_error)
            raise GSheetExportError(message_error)

