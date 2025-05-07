import requests
import xml.etree.ElementTree as ET


NAMESPACE = {
    'default': 'http://www.sitemaps.org/schemas/sitemap/0.9',
    'image': 'http://www.google.com/schemas/sitemap-image/1.1'
}
    


class Product:
    """
    Represents a product from the Baker website.
    """

    def __init__(self, url, title, image, lastmod, changefreq):
        self.url = url
        self.title = title
        self.lastmod = lastmod
        self.changefreq = changefreq
        self.image = image
    
    
    @classmethod
    def from_urlmap(cls, urlmap):
        url = urlmap.find('default:loc').text
        title = urlmap.find('default:title').text
        image = urlmap.find('image:loc').text
        lastmod = urlmap.find('default:lastmod').text
        changefreq = urlmap.find('default:changefreq').text
        return cls(url, title, image, lastmod, changefreq)


class Baker():


    sitemap = 'https://bakerskateboards.com/sitemap.xml'
    

    @classmethod
    def get_root_sitemap(cls):
        response = requests.get(cls.sitemap)
        if response.status_code == 200:
            return ET.fromstring(response.text)
        else:
            raise Exception(f"Failed to get root sitemap: {response.status_code} + {response.text}")
    
    
    @classmethod
    def get_products_sitemap(cls):
        sitemap = cls.get_root_sitemap()
        for loc in sitemap.findall(f"default:sitemap/default:loc", cls.namespaces):
            if 'products' in loc.text:
                response = requests.get(loc.text)
                if response.status_code == 200:
                    return ET.fromstring(response.text)
                else:
                    raise Exception(f"Failed to get products sitemap: {response.status_code} + {response.text}")
        raise Exception("No products sitemap found")


    @classmethod
    def get_products(cls):
        sitemap = cls.get_products_sitemap()
        for product in sitemap.findall(f"default:url/default:loc", NAMESPACE):
            pass


    @classmethod
    def scan(cls):
        pass

