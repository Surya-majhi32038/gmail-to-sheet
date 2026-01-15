from src.gmail_service import get_gmail_service, fetch_unread_emails
from src.email_parser import parse_email



def main():
    service = get_gmail_service()
    print("Gmail service created:", service is not None)
    emails = fetch_unread_emails(service, max_results=5)
    # parsed = parse_email(emails)
    print(emails)
    # print(emails)
    # print(service)

if __name__ == "__main__":
    main()

