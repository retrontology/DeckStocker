from stocker.providers.baker import Baker
from stocker.providers.nocomply import NoComply
from stocker.product import ItemAvailability


baker = Baker()
nocomply = NoComply()


products = nocomply.get_products()

for product in products:
    for offer in product.offers:
        if offer.availability != ItemAvailability.IN_STOCK:
            print(f'{product.name} - {offer.name} - {offer.availability}')
