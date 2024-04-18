
import os
from db import Database
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from db import Database

load_dotenv()


def get_data(db:Database):
    page_num = 1
    stop = False
    star_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5}
    while not stop:
        URL= f'https://books.toscrape.com/catalogue/page-{page_num}.html'
        page_num += 1
        res = requests.get(URL)
        if res.status_code != 200:
            stop = True
            return
        soup = BeautifulSoup(res.text, 'html.parser')
        book_list = soup.select('article.product_pod')
        for book in book_list:
            title = book.select_one('img')['alt']
            star = star_dict[book.select_one('p')['class'][-1].lower()]
            price = book.select_one('p.price_color').text[2:]
            in_stock = 'In Stock' if 'in stock' in book.text.lower() else 'Out of Stock' 
            image_url = book.select_one('img')['src']
            # print(title, star, price, in_stock, image_url)
            book = {}
            book['title'], book['star'], book['price'], book['in_stock'], book['url'] = title, star, price, in_stock, image_url
            db.insert_book(book)

with Database(os.getenv('DATABASE_URL')) as db:
    db.truncate_table()
    db.create_table()
    get_data(db)
    