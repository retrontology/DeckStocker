from typing import Self, List, Dict
from enum import Enum
from datetime import datetime
#from influxdb_client import Point


class ItemAvailability(Enum):
    """
    Represents the availability of an item.
    """


    BACK_ORDER = 'https://schema.org/BackOrder'
    DISCONTINUED = 'https://schema.org/Discontinued'
    IN_STOCK = 'https://schema.org/InStock'
    IN_STORE_ONLY = 'https://schema.org/InStoreOnly'
    LIMITED_AVAILABILITY = 'https://schema.org/LimitedAvailability'
    MADE_TO_ORDER = 'https://schema.org/MadeToOrder'
    ONLINE_ONLY = 'https://schema.org/OnlineOnly'
    OUT_OF_STOCK = 'https://schema.org/OutOfStock'
    PRE_ORDER = 'https://schema.org/PreOrder'
    PRE_SALE = 'https://schema.org/PreSale'
    RESERVED = 'https://schema.org/Reserved'
    SOLD_OUT = 'https://schema.org/SoldOut'


    def __str__(self) -> str:
        return self.name


class ProductImage:
    """
    Represents an image of a product.

    Attributes:
        url (str): The URL of the image.
        name (str): The name of the image.
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
    """


    def __init__(self, url: str, name: str, width: int, height: int) -> None:
        self.url = url
        self.name = name
        self.width = width
        self.height = height


    def __str__(self) -> str:
        return f'{self.name} ({self.width}x{self.height})'


    @classmethod
    def from_json(cls, json: dict) -> Self:
        return cls(
            url=json['url'],
            name=json['name'],
            width=json['width'],
            height=json['height']
        )


class ProductOffer:
    """
    Represents an offering/variant of a product.

    Attributes:
        name (str): The name of the product offer.
        availability (ItemAvailability): The availability of the product offer.
        price (float): The price of the product offer.
        price_currency (str): The currency of the price.
        price_valid_until (datetime): The date and time until which the price is valid.
        sku (str): The stock keeping unit of the product offer.
        url (str): The URL of the product offer.
    """

    def __init__(
        self,
        name: str,
        availability: ItemAvailability,
        price: float,
        price_currency: str,
        price_valid_until: datetime,
        sku: str,
        url: str,
        
    ) -> None:
        self.name = name
        self.availability = availability
        self.price = price
        self.price_currency = price_currency
        self.price_valid_until = price_valid_until
        self.sku = sku
        self.url = url
    

    @classmethod
    def from_json(cls, json: dict) -> Self:
        """
        Create a ProductOffer from a JSON object.
        """
        return cls(
            name=json['name'],
            availability=ItemAvailability(json['availability']),
            price=json['price'],
            price_currency=json['priceCurrency'],
            price_valid_until=datetime.fromisoformat(json['priceValidUntil']),
            sku=json['sku'],
            url=json['url'],
        )


    def __str__(self) -> str:
        return f'{self.name} ({self.availability})'


class Product():
    """
    Represents a product from a provider.
    """

    def __init__(
        self,
        offers: List[ProductOffer],
        brand: Dict[str, str],
        name: str,
        description: str,
        category: str,
        url: str,
        sku: str,
        image: ProductImage,
    ) -> None:
        self.offers = offers
        self.brand = brand
        self.name = name
        self.description = description
        self.category = category
        self.url = url
        self.sku = sku
        self.image = image
    

    def __str__(self) -> str:
        return f'{self.name} ({self.url})'
    

    @classmethod
    def from_json(cls, json: dict) -> Self:
        offers = [ProductOffer.from_json(offer) for offer in json['offers']]
        return cls(
            offers=offers,
            brand=json['brand'],
            name=json['name'],
            description=json['description'],
            category=json['category'],
            url=json['url'],
            sku=json['sku'],
            image=ProductImage.from_json(json['image'])
        )
