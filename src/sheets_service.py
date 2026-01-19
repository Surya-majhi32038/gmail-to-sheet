from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from config import (
    GMAIL_SCOPES,
    TOKEN_FILE,
    SPREADSHEET_ID,
    SHEET_NAME
)


# ---------------------------------
# 1. AUTHENTICATE SHEETS SERVICE
# ---------------------------------

def get_sheets_service():
    """
    Create and return Google Sheets API service.
    """
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, GMAIL_SCOPES)
    service = build("sheets", "v4", credentials=creds)
    return service


# ---------------------------------
# 2. FORMAT EMAIL DATA FOR SHEET
# ---------------------------------

def format_row_data(parsed_email):
    """
    Convert parsed email dictionary into a row list.
    """
    return [
        parsed_email.get("from", ""),
        parsed_email.get("subject", ""),
        parsed_email.get("date", ""),
        parsed_email.get("content", "")
    ]


# ---------------------------------
# 3. APPEND ROW TO GOOGLE SHEET
# ---------------------------------

def append_row(service, row_data):
    """
    Append a single row to the Google Sheet.
    """
    body = {
        "values": [row_data]
    }

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()


# ---------------------------------
# 4. HIGH-LEVEL FUNCTION
# ---------------------------------

def append_email_to_sheet(parsed_email):
    """
    Orchestrates appending parsed email to Google Sheet.
    """
    service = get_sheets_service()
    row_data = format_row_data(parsed_email)
    append_row(service, row_data)
