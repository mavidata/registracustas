import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from pandas import DataFrame

from utils.variables import (
    hotel_project_id,
    hotel_project_client_email,
    hotel_project_client_id,
    hotel_private_key_id,
    hotel_private_key
)


class GoogleSheets:
    def __init__(self, service_account_info, sheet_id):
        self.service_account_info = service_account_info
        self.sheet_id = sheet_id
        self.scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    def __authorize(self):
        credentials = Credentials.from_service_account_info(
            info=self.service_account_info, scopes=self.scopes
        )
        client = gspread.authorize(credentials)
        return client


    def append(self, sheet_name, dataframe: DataFrame):
        client = self.__authorize()
        sheet = client.open_by_key(self.sheet_id)
        worksheet = sheet.worksheet(sheet_name)

        existing_rows = len(worksheet.get_all_values())

        start_row = existing_rows + 1 if existing_rows > 0 else 1

        set_with_dataframe(
            worksheet,
            dataframe.reset_index(drop=True),
            include_column_header=(existing_rows == 0),  
            row=start_row,
            col=1
        )


class HotelMakerGoogleSheets(GoogleSheets):
    def __init__(self):
        service_account_info = {
            "type": "service_account",
            "project_id": hotel_project_id,
            "private_key_id": hotel_private_key_id,
            "private_key": hotel_private_key,
            "client_email": hotel_project_client_email,
            "client_id": hotel_project_client_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{hotel_project_client_email}",
            "universe_domain": "googleapis.com",
        }
        sheet_id = "1Qc_83GVDHBZyXJIEHAGtjvy5TI7norflFlT-EW_4MCg"
        super().__init__(service_account_info, sheet_id)

