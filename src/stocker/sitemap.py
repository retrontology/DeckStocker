import requests
import xml.etree.ElementTree as ET
import logging
from typing import Self, Generator
from datetime import datetime



DEFAULT_NAMESPACE = {
    'default': 'http://www.sitemaps.org/schemas/sitemap/0.9',
    'image': 'http://www.google.com/schemas/sitemap-image/1.1'
}


class ProductURL():
    """
    A class representing a product URL from a sitemap.

    Attributes:
        url (str): The URL of the product.
        last_modified (datetime): The last modified date of the product.
        change_frequency (str): The change frequency of the product.
        image_url (str): The URL of the product image.
        image_title (str): The title of the product image.
        image_caption (str): The caption of the product image.
    """

    def __eq__(self, other: Self) -> bool:
        """
        Checks if two ProductURL objects are equal.
        """
        return (
            self.url == other.url and
            self.last_modified == other.last_modified and
            self.change_frequency == other.change_frequency and
            self.image_url == other.image_url and
            self.image_title == other.image_title and
            self.image_caption == other.image_caption
        )


    def __init__(self, url:str, last_modified:datetime, change_frequency:str, image_url:str, image_title:str, image_caption:str) -> None:
        """
        Initializes a Product object.

        Args:
            url (str): The URL of the product.
            last_modified (datetime): The last modified date of the product.
            change_frequency (str): The change frequency of the product.
            image_url (str): The URL of the product image.
            image_title (str): The title of the product image.
            image_caption (str): The caption of the product image.
        """
        self.url = url
        self.last_modified = last_modified
        self.change_frequency = change_frequency
        self.image_url = image_url
        self.image_title = image_title
        self.image_caption = image_caption
    
    
    @classmethod
    def from_xml(cls, xml_element: ET.Element, namespaces: dict = DEFAULT_NAMESPACE) -> Self:
        """
        Creates a Product object from an XML element.
        Args:
            xml_element (ElementTree.Element): The XML element to create the Product object from.
        Returns:
            Product: A Product object.
        """
        return cls(
            url=xml_element.find('default:loc', namespaces).text,
            last_modified=datetime.strptime(xml_element.find('default:lastmod', namespaces).text, '%Y-%m-%dT%H:%M:%S%z'),
            change_frequency=xml_element.find('default:changefreq', namespaces).text,
            image_url=xml_element.find('image:image/image:loc', namespaces).text,
            image_title=xml_element.find('image:image/image:title', namespaces).text,
            image_caption=xml_element.find('image:image/image:caption', namespaces).text,
        )


class SitemapCrawler():
    """
    A sitemap crawler for finding product pages on a website.
    """

    def __init__(self, root_url, xml_namespaces=DEFAULT_NAMESPACE):
        """
        Initializes the sitemap crawler with the root URL of the website and optional XML namespaces.
        Args:
            root_url (str): The URL of the website's root sitemap
            xml_namespaces (dict, optional): A dictionary of XML namespaces to use when parsing the sitemap. Defaults to DEFAULT_NAMESPACE.
        """
        self.root = root_url
        self.namespaces = xml_namespaces
        self.logger = logging.getLogger(f'{self.__class__.__name__}.{root_url}')
    

    def _get_root_sitemap(self):
        """
        Internal method to fetch and parse the root sitemap.
        Returns:
            ElementTree.Element: The parsed XML tree of the root sitemap.
        """
        response = requests.get(self.root)
        if response.status_code == 200:
            return ET.fromstring(response.text)
        else:
            raise Exception(f"Failed to get root sitemap: {response.status_code} + {response.text}")
    
    
    def get_products_sitemap(self):
        """
        Fetches and parses the products sitemap.
        Returns:
            ElementTree.Element: The parsed XML tree of the products sitemap.
        """
        sitemap = self._get_root_sitemap()
        for loc in sitemap.findall(f"default:sitemap/default:loc", self.namespaces):
            if 'products' in loc.text:
                response = requests.get(loc.text)
                if response.status_code == 200:
                    return ET.fromstring(response.text)
                else:
                    raise Exception(f"Failed to get products sitemap: {response.status_code} + {response.text}")
        raise Exception("No products sitemap found")
    

    def get_products(self) -> Generator[ProductURL, None, None]:
        """
        Fetches and parses the products sitemap.
        Returns:
            Generator[ProductURL, None, None]: A generator of ProductURL objects.
        """
        sitemap = self.get_products_sitemap()
        for product_url in sitemap.findall(f"default:url", self.namespaces):
            try:
                yield ProductURL.from_xml(product_url, self.namespaces)
            except Exception as e:
                self.logger.error(f"Error parsing product: {e}")
