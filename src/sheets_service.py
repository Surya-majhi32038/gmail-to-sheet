from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.utils import parseaddr
from email.utils import parsedate_to_datetime
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
    from_data = parsed_email.get("from", "")
    email_address = parseaddr(from_data)[1]

    # date 
    

    date_data = parsed_email.get("date", "")

    try:
        date_obj = parsedate_to_datetime(date_data)
        date_obj = date_obj.replace(tzinfo=None)
        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        formatted_date = "Unknown"


    payload = parsed_email.get("content", {})
   
    email_text = clean_email_content(payload)
  

    return [
        email_address,
        parsed_email.get("subject", "").strip(),
        formatted_date,
        email_text
    ]


import re

def clean_email_content(html: str) -> str:
    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    #  remove unwanted tags completely
    for tag in soup(["style", "script", "head", "meta", "title", "img"]):
        tag.decompose()

    #  get readable text
    text = soup.get_text(separator="\n")

    #  clean junk
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)

    # remove leftover links
    text = re.sub(r"https?://\S+", "", text)

    #  remove image markers
    text = re.sub(r"\[image:[^\]]*\]", "", text, flags=re.I)

    # final cleanup
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    return "\n".join(lines)



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
