from abc import ABC, abstractmethod


class WebsiteProvider(ABC):

    @abstractmethod
    def lookup(self, business_name, town):
        raise NotImplementedError
