# src/gmail_service.py

import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from config import GMAIL_SCOPES
from config import CREDENTIALS_FILE, TOKEN_FILE


def get_gmail_service():
    creds = None

    # ✅ Load existing token (JSON)
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE, GMAIL_SCOPES
        )

    # ✅ If token is invalid or missing
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, GMAIL_SCOPES
            )
            creds = flow.run_local_server(port=0)

        # ✅ Save token as UTF-8 JSON
        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_unread_emails(service, max_results=10):
    """
    Fetches unread emails from Gmail Inbox.
    Marks them as read after fetching.
    Returns a list of message objects.
    """

    response = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=max_results
    ).execute()

    messages = response.get("messages", [])

    if not messages:
        print("No unread emails found.")
        return []

    email_data = []

    for msg in messages:
        msg_id = msg["id"]

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
