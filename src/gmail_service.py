# src/gmail_service.py

import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import GOOGLE_SHEETS_SCOPS, GMAIL_SCOPS
from config import CREDENTIALS_FILE, TOKEN_FILE

# TOKEN_FILE = "token_gmail.pickle"
# CREDENTIALS_FILE = "credentials/credentials.json"


def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, GMAIL_SCOPS
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service

def fetch_unread_emails(service, max_results=10):
    """
    Fetches unread emails from Gmail Inbox.
    Marks them as read after fetching.
    Returns a list of message objects.
    """
    # Search only unread emails in Inbox
    response = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=max_results
    ).execute()

    messages = response.get("messages", [])

    if not messages:
        print(" No unread emails found.")
        return []

    email_data = []

    for msg in messages:
        msg_id = msg["id"]

        # Get full message
        message = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

        email_data.append(message)

        # Mark email as READ
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

    return email_data