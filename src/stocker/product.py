from typing import Self
from stocker.sitemap import ProductURL


class Product():
    """
    Represents a product from a provider.
    """

    def __init__(self, name: str, url: str, image_url: str, in_stock: bool, price: float, variant: str = None) -> None:
        """
        Initializes the product with the product URL.

        Args:
            name (str): The name of the product.
            url (str): The product URL.
            image_url (str): The image URL of the product.
            in_stock (bool): Whether the product is in stock.
            price (float): The price of the product.
            variant (str, optional): The variant identifier (e.g., "Size: M, Color: Blue"). Defaults to None.
        """
        self.name = name
        self.url = url
        self.image_url = image_url
        self.in_stock = in_stock
        self.price = price
        self.variant = variant
    

    @classmethod
    def from_product_url(cls, product_url: ProductURL, in_stock: bool, price: float, variant: str = None) -> Self:
        """
        Creates a product from a product URL.
        """
        return cls(
            name=product_url.image_title,
            url=product_url.url,
            image_url=product_url.image_url,
            in_stock=in_stock,
            price=price,
            variant=variant
        )