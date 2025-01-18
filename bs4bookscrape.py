import requests
from bs4 import BeautifulSoup

book_url = 'https://books.toscrape.com/'

response = requests.get(book_url)
response.encoding = 'utf - 8'

soup = BeautifulSoup(response.text,'html.parser')

#name, price, category, stars, upc, availability, in_stock, image_link
name = soup.find('div', class_='product_main').h1.text
print(name)

price = soup.find('div', class_='product_main').p.text
print(price)









