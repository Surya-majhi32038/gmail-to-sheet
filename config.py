# config.py

# Google Sheets configuration
SPREADSHEET_ID = "10Boxcjk_wOIzxUQlee7Yn_lGV0xMPzmzMYgceITUku8"

# Sheet name (tab name)
SHEET_NAME = "Sheet1"   # or whatever you named the tab

# OAuth scopes
GMAIL_SCOPS = [
    "https://www.googleapis.com/auth/gmail.modify",
]
GOOGLE_SHEETS_SCOPS = ["https://www.googleapis.com/auth/spreadsheets"]
# Credential paths
CREDENTIALS_FILE = "credentials/credentials.json"
TOKEN_FILE = "credentials/token.json"
