from stocker.sitemap import SitemapCrawler, ProductURL
from typing import Generator, List
import logging
import requests
from bs4 import BeautifulSoup
from stocker.product import Product

class BaseProvider:
    """
    Represents a base provider for fetching data from a website.

    Attributes:
        sitemap_url (str): The URL of the root sitemap.
        sitemap_crawler (SitemapCrawler): The sitemap crawler class.
    """


    sitemap_url: str
    sitemap_crawler: SitemapCrawler = SitemapCrawler


    def __init__(self) -> None:
        """
        Initializes the provider with the sitemap URL.
        """
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.sitemap = self.sitemap_crawler(self.sitemap_url)


    def get_products(self) -> Generator[ProductURL, None, None]:
        """
        Retrieves all product URLs from the sitemap.

        Returns:
            Generator[ProductURL, None, None]: A generator of product URLs.
        """
        product_urls = self.sitemap.get_products()
        for product_url in product_urls:
            yield self.get_product(product_url)


    def get_product(self, product_url: ProductURL) -> List[Product]:
        """
        Retrieves a product page from the provider and parses it to get the product information.

        Args:
            product_url (ProductURL): The product URL.

        Returns:
            List[Product]: A list of products, one for each variant.
        """
        response = requests.get(product_url.url)
        if response.status_code != 200:
            raise Exception(f"Failed to get product page: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Get all variants for this product
        variants = self.parse_variants(soup)
        
        if not variants:
            # If no variants found, treat as single product
            in_stock = self.parse_stock_status(soup)
            price = self.parse_price(soup)
            return [Product.from_product_url(product_url, in_stock, price)]
        
        products = []
        for variant in variants:
            in_stock = self.parse_stock_status(soup, variant)
            price = self.parse_price(soup, variant)
            products.append(Product.from_product_url(product_url, in_stock, price, variant))
        
        return products


    def parse_variants(self, soup: BeautifulSoup) -> List[str]:
        """
        Parses the variants from the product page. Should be implemented by child classes.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the product page.

        Returns:
            List[str]: A list of variant identifiers.
        """
        pass


    def parse_stock_status(self, soup: BeautifulSoup, variant: str = None) -> bool:
        """
        Parses the stock status from the product page. Should be implemented by child classes.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the product page.
            variant (str, optional): The variant identifier. Defaults to None.

        Returns:
            bool: Whether the product is in stock.
        """
        pass


    def parse_price(self, soup: BeautifulSoup, variant: str = None) -> float:
        """
        Parses the price from the product page. Should be implemented by child classes.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the product page.
            variant (str, optional): The variant identifier. Defaults to None.

        Returns:
            float: The price of the product.
        """
        pass
