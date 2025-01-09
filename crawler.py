import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler.settings")
django.setup()

from products.models import Product
import json

import requests
from bs4 import BeautifulSoup

final_products = []

page = requests.get('https://dgtamin.com/product-category/electronic-devices/mobile/mobile-xiaomi/')
if page.status_code==200:
    soup = BeautifulSoup(page.text, "html.parser")

    products = soup.find_all('div', attrs={'class': 'products__item-img-color-wrapper'}, limit=5)
    for product in products:
        img = product.find('div', attrs={'class': 'products__item-image-wrapper has_second'}).find('a').find('img', attrs={'class': 'products__item-image entered lazyloaded'})['src']
        title = product.find('div', attrs={'class': 'products__item-info'}).find('p').find('a')['title']
        final_products.append({"title": title, "img": img})
    
    import json
    with open("products.json", "w", encoding="utf-8") as file:
        json.dump(final_products, file, ensure_ascii=False, indent=4)

    print("Scraped products:", final_products)
else:
    print("Request not Succsess!")
    print(page.text)

page = requests.get('https://basalam.com/subcategory/power-tools')
if page.status_code==200:
    soup = BeautifulSoup(page.text, "html.parser")

    products = soup.find_all('div', attrs={'class': 'BMuJ5D _0UvDlh _1n_6H7'}, limit=50)
    for product in products:
        title = product.find('div', attrs={'class': '_3YTkz_'}).find('a', attrs={'class': '_5PwYIn Sh2LgL'}).text
        img = product.find('div', attrs={'class': 'ssEXuG'}).find('a').find('img')["src"]
        final_products.append({"title": title, "img": img})
    
    import json
    with open("products.json", "w", encoding="utf-8") as file:
        json.dump(final_products, file, ensure_ascii=False, indent=4)

    print("Scraped products:", final_products)
else:
    print("Request not Succsess!")
    print(page.text)

with open("products.json", "w", encoding="utf-8") as file:
    json.dump(final_products, file, ensure_ascii=False, indent=4)

for product in final_products:
    Product.objects.get_or_create(title=product["title"], image=product["img"])

print("Products saved to database.")