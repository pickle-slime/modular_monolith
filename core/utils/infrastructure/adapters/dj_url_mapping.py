from django.urls import reverse

from core.utils.domain.interfaces.hosts.url_mapping import URLHost

class DjangoURLAdapter(URLHost):
    def get_absolute_url_of_product(self, category_slug: str, product_slug: str) -> str:
        return reverse("product", kwargs={"category": category_slug, "product": product_slug})

    def get_absolute_url_of_category(self, category_slug: str) -> str:
        return reverse("category", kwargs={"category": category_slug})

    def get_absolute_url_of_brand(self, brand_slug: str) -> str:
        return reverse("brand", kwargs={"brand": brand_slug})