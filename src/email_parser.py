import base64


# -------------------------------
# 1. HEADER EXTRACTION UTILITIES
# -------------------------------

def get_headers(message):
    """
    Safely get headers list from Gmail message.
    """
    payload = message.get("payload", {})
    return payload.get("headers", [])


def get_header_value(headers, header_name):
    """
    Extract a specific header value (From, Subject, Date).
    """
    for header in headers:
        if header.get("name", "").lower() == header_name.lower():
            return header.get("value", "")
    return ""


def extract_sender(headers):
    return get_header_value(headers, "From")


def extract_subject(headers):
    return get_header_value(headers, "Subject")


def extract_date(headers):
    return get_header_value(headers, "Date")


# -------------------------------
# 2. BODY DECODING UTILITIES
# -------------------------------

def decode_base64(data):
    """
    Decode base64 encoded email body safely.
    """
    if not data:
        return ""

    decoded_bytes = base64.urlsafe_b64decode(data)
    return decoded_bytes.decode("utf-8", errors="ignore")


def extract_body_from_simple_email(payload):
    """
    Extract body when email is not multipart.
    """
    body_data = payload.get("body", {}).get("data")
    return decode_base64(body_data)


def extract_body_from_multipart_email(payload):
    """
    Extract plain text body from multipart email.
    """
    parts = payload.get("parts", [])

    for part in parts:
        if part.get("mimeType") == "text/plain":
            body_data = part.get("body", {}).get("data")
            return decode_base64(body_data)

    return ""


def extract_email_body(payload):
    """
    Decide whether email is simple or multipart and extract body.
    """
    if payload.get("body", {}).get("data"):
        return extract_body_from_simple_email(payload)
    else:
        return extract_body_from_multipart_email(payload)


# starting point
# 
def parse_email(message):
    """
    Convert raw Gmail message into structured data.
    """
    payload = message.get("payload", {})
    headers = get_headers(message)

    email_data = {
        "from": extract_sender(headers),
        "subject": extract_subject(headers),
        "date": extract_date(headers),
        "content": extract_email_body(payload),
    }

    return email_data
