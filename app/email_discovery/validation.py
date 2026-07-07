import re

INVALID_PLACEHOLDERS = {
    "test@test.com",
    "example@example.com",
    "info@example.com",
    "hello@example.com",
    "email@example.com",
}

BLOCKED_DOMAINS = {
    "sentry.io",
    "wixpress.com",
    "google.com",
}

BLOCKED_KEYWORDS = {
    "sentry",
    "ingest",
    "noreply",
    "no-reply",
    "donotreply",
    "do-not-reply",
}

EMAIL_PATTERN = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.I)


def is_valid_email(email):
    email = str(email).strip().lower()

    if not email:
        return False, "Email is blank"

    if email in INVALID_PLACEHOLDERS:
        return False, "Placeholder email"

    if "example.com" in email:
        return False, "Example domain"

    if not EMAIL_PATTERN.match(email):
        return False, "Invalid email format"

    local, domain = email.split("@", 1)

    if domain in BLOCKED_DOMAINS or any(domain.endswith("." + d) for d in BLOCKED_DOMAINS):
        return False, "Blocked technical/domain email"

    if any(keyword in email for keyword in BLOCKED_KEYWORDS):
        return False, "Blocked technical email"

    return True, "Valid"
