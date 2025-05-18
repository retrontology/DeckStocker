from stocker.providers.base import BaseProvider
from bs4 import BeautifulSoup


class Baker(BaseProvider):


    sitemap_url = 'https://bakerskateboards.com/sitemap.xml'


    def parse_stock_status(self, soup: BeautifulSoup) -> bool:
        """
        Parses the stock status from the product page.
        """
        return soup.find('button', class_='ProductForm__AddToCart').text.strip() == 'Add to cart'


    def parse_price(self, soup: BeautifulSoup) -> float:
        """
        Parses the price from the product page.
        """
        return float(soup.find('span', class_='ProductMeta__Price').text.strip().replace('$', ''))
