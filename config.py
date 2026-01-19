# config.py

# Google Sheets configuration
SPREADSHEET_ID = "1nUIJVuCXt4LpnK290UHjEBWjw1rbObJ87zS2Zn4Lbv4"

# Sheet name (tab name)
SHEET_NAME = "Sheet1"   # or whatever you named the tab

# OAuth scopes
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets"
]
# Credential paths
CREDENTIALS_FILE = "credentials/credentials.json"
TOKEN_FILE = "credentials/token.json"
