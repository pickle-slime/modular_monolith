from .base_host import BaseHost

from abc import abstractmethod

class URLHost(BaseHost):
    @abstractmethod
    def get_absolute_url_of_product(self, category_slug: str, product_slug: str) -> str:
        pass

    @abstractmethod
    def get_absolute_url_of_category(self, category_slug: str) -> str:
        pass

    @abstractmethod
    def get_absolute_url_of_brand(self, brand_slug: str) -> str:
        pass
