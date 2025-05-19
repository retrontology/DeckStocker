from stocker.sitemap import SitemapCrawler, ProductURL
from typing import Generator, List
import json
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
        name (str): The name of the provider.
    """

    sitemap_url: str
    sitemap_crawler: SitemapCrawler = SitemapCrawler
    name: str

    def __init__(self) -> None:
        """
        Initializes the provider with the sitemap URL.
        """
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.sitemap = self.sitemap_crawler(self.sitemap_url)
        self.name = self.__class__.__name__


    def _get_page(self, url: str) -> BeautifulSoup:
        """
        Retrieves a page from the provider and returns a BeautifulSoup object.
        """
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to get product page: {response.status_code}")
        return BeautifulSoup(response.text, 'html.parser')


    def _get_product_json(self, url: str) -> dict:
        """
        Retrieves the product JSON data from a product page.
        """
        soup = self._get_page(url)
        product_json = soup.find('script', type='application/ld+json')
        if not product_json:
            raise Exception("No product JSON found")
        return json.loads(product_json.text)
        

    def get_products(self) -> Generator[Product]:
        """
        Retrieves all products from the provider and returns a generator of Products.
        """
        for product_url in self.sitemap.get_product_urls():
            product_json = self._get_product_json(product_url.url)
            yield Product.from_json(product_json)
    
