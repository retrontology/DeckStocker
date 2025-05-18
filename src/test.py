from stocker.providers.baker import Baker


baker = Baker()


products = baker.get_products()

for product in products:
    if not product.in_stock:
        print(product)
