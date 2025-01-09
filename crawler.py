import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler.settings")
django.setup()

from products.models import Product
import json
import requests
from bs4 import BeautifulSoup

final_products = []

page = requests.get('https://sabzlearn.ir/courses/')
if page.status_code==200:
    soup = BeautifulSoup(page.text, "html.parser")

    products = soup.find_all('div', attrs={'class': 'course flex flex-col bg-white dark:bg-darker rounded-xl'}, limit=50)
    for product in products:
        title = product.find('div', attrs={'class': 'flex-grow px-4.5 pt-4 pb-3'}).find('h3').find('a').text
        img = product.find('a', attrs={'class': 'block h-42'}).find('img')['src']
        final_products.append({"title": title, "img": img})

else:
    print("Request not Succsess!")
    print(page.text)


page = requests.get('https://maktabkhooneh.org/learn/programming-languages/')
if page.status_code==200:
    soup = BeautifulSoup(page.text, "html.parser")

    products = soup.find_all('a', attrs={'class': 'search-course-card flex items-start rounded-lg p-8 md:p-12 bg-white gap-12 sm:gap-16 search-course-card__container-height'}, limit=5)
    for product in products:
        title = product.find('div', attrs={'class': 'flex-1 flex flex-col h-full'}).find('div', attrs={'class': 'flex justify-between items-center'}).find('h2').text
        try:
            img = product.find('span', attrs={'class': 'relative rounded-md flex aspect-square sm:aspect-9/5 search-course-card__img'}).find('img')['src']
        except:
            img = "No Image"
        final_products.append({"title": title, "img": img})

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

else:
    print("Request not Succsess!")
    print(page.text)

with open("products.json", "w", encoding="utf-8") as file:
    json.dump(final_products, file, ensure_ascii=False, indent=4)

for product in final_products:
    Product.objects.get_or_create(title=product["title"], image=product["img"])

print("Products saved to database.")
