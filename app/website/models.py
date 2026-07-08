from dataclasses import dataclass


@dataclass
class WebsiteData:
    website: str | None = None
    phone: str | None = None
    email: str | None = None
    facebook: str | None = None
    instagram: str | None = None
