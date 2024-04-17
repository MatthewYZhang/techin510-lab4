import os
from db import Database
import streamlit as st
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup # type: ignore
from db import Database
import sys
import argparse

load_dotenv()
db = Database(os.getenv('DATABASE_URL'))
db.create_table()

parser = argparse.ArgumentParser()
parser.add_argument('--fetch_data', type=bool, default=False)
args = parser.parse_args()

def get_data():
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
            print(title, star, price, in_stock, image_url)
            book = {}
            book['title'], book['star'], book['price'], book['in_stock'], book['url'] = title, star, price, in_stock, image_url
            db.insert_book(book)

if args.fetch_data:
    get_data()

def display_books(books):
    if not books:
        return
    for book in books:
        with st.expander(f'{book[1]} {":star:" * book[2]}'):
            st.image(f'https://books.toscrape.com/{book[5][3:]}')
            st.markdown(f'''
- Price: {book[3]} pounds 
- {book[4]}
            ''')

st.title('Book Display')
st.subheader('A simple app to webscrap a book website and display all infos')

st.markdown('---')

# books = db.query_table()

# Search, sort, and filter bar
search_query = st.text_input("Search books")
sort_column = st.selectbox("Sort by", ["title", "star", "price"], index=1)
sort_order = st.selectbox("Order by", ["from high to low", "from low to high"], index=0)
filter_in_stock = st.checkbox("Filter In Stock Only")

books = db.query_table(search_query, sort_column, sort_order, filter_in_stock)

display_books(books)

# sys.exit()