# config.py

# Google Sheets configuration
SPREADSHEET_ID = "10Boxcjk_wOIzxUQlee7Yn_lGV0xMPzmzMYgceITUku8"

# Sheet name (tab name)
SHEET_NAME = "Sheet1"   # or whatever you named the tab

# OAuth scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets",
]

# Credential paths
CREDENTIALS_FILE = "credentials/credentials.json"
TOKEN_FILE = "credentials/token.json"
