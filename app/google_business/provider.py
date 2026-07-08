from abc import ABC, abstractmethod

from app.google_business.models import GoogleBusinessData


class GoogleBusinessProvider(ABC):
    @abstractmethod
    def search(self, business_name: str, town: str) -> GoogleBusinessData:
        """
        Return Google Business information for a business.

        Returns an empty GoogleBusinessData object if nothing is found.
        """
        raise NotImplementedError
