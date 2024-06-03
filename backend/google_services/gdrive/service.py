import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from utils.logger import logger


class GDriveService:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.service = None

    def authenticate(self):
        creds = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=["https://www.googleapis.com/auth/drive.readonly"]
        )

        self.service = build("drive", "v3", credentials=creds)

    def download_images_from_folder(self, folder_id, save_path):
        try:
            results = self.service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name)").execute()
            files = results.get("files", [])

            if not os.path.exists(save_path):
                os.makedirs(save_path)

            for file in files:
                file_id = file["id"]
                file_name = file["name"]

                request = self.service.files().get_media(fileId=file_id)
                save_file_path = os.path.join(save_path, file_name)

                with open(save_file_path, "wb") as f:
                    media_request = MediaIoBaseDownload(f, request)
                    while True:
                        try:
                            download_progress, done = media_request.next_chunk()
                        except Exception as e:
                            logger.error(f"An error occurred while downloading '{file_name}': {str(e)}")
                            break

                        if done:
                            logger.debug(f"Download of '{file_name}' completed successfully.")
                            break

        except Exception as e:
            logger.error(f"An error occurred while listing files: {str(e)}")







