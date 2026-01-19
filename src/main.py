from src.gmail_service import get_gmail_service, fetch_unread_emails
from src.email_parser import parse_email
from src.sheets_service import append_email_to_sheet


def main():
    service = get_gmail_service()
    print("Gmail service created:", service is not None)
    emails = fetch_unread_emails(service, max_results=10)
    # just for testing
    print("Fetched emails:",len(emails))
    # p = parse_email(emails[0])
    # append_email_to_sheet(p)
    # print("Parsed email:",p)
    for message in emails:
        parsed_email = parse_email(message)
        append_email_to_sheet(parsed_email)
        # print(parsed_email)
        # append_email_to_sheet(parsed_email)
    # parsed = parse_email(emails)
    # print(emails)
    # print(emails)
    # print(service)

if __name__ == "__main__":
    main()

