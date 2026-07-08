from dataclasses import dataclass
from typing import Optional


@dataclass
class WebsiteData:
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
