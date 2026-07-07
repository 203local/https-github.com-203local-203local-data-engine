import re

INVALID_PLACEHOLDERS = {
    "test@test.com",
    "example@example.com",
    "info@example.com",
    "hello@example.com",
    "email@example.com",
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

    return True, "Valid"
