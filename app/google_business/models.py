from dataclasses import dataclass
from typing import Optional


@dataclass
class GoogleBusinessData:
    maps_url: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    price_level: Optional[str] = None
    hours: Optional[dict] = None
    categories: Optional[list] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
