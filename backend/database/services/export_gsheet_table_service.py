from typing import List, Optional

from config.settings import settings
from google_services.gsheet.service import (
    GoogleSheetService
)
from google_services.gsheet.exceptions import (
    GSheetExportError,
    GSheetAuthError,
    GSheetLoadError
)
from utils.logger import logger


class ExportGSheetTableService:
    def __init__(self, link_to_worksheet, credentials_path):
        self.link_to_worksheet = link_to_worksheet
        self.gsheet_service = GoogleSheetService(credentials_path)
        self.list_of_dict = []

    @staticmethod
    def convert_list_to_dict_list(data: list, headers: list):
        result_list = []

        for row in data:
            data_dict = {}
            for idx, header in enumerate(headers):
                data_dict[header] = row[idx]

            result_list.append(data_dict)

        return result_list

    async def _auth_and_load_sheet(self):
        self.gsheet_service.authenticate()
        self.gsheet_service.load_sheet(self.link_to_worksheet)

    async def export_table(self, validator) -> Optional[List]:
        """Returns True if export is successful, False otherwise"""
        try:
            await self._auth_and_load_sheet()
            exported_data = self.gsheet_service.export_data_from_worksheet()
            table_headers = exported_data[0]
            self.list_of_dict = self.convert_list_to_dict_list(
                data=exported_data[1:],
                headers=table_headers
            )
            # return [validator(**row_dict) for row_dict in self.list_of_dict]
            locations = []
            for row_dict in self.list_of_dict:
                try:
                    locations.append(validator(**row_dict))
                except Exception as ex:
                    logger.error(f'Error validate: {row_dict}: {ex}')

            return locations

        except GSheetAuthError as e:
            ...

        except GSheetLoadError as e:
            ...

        except GSheetExportError as e:
            ...

        return None
