import os
from db import Database
import streamlit as st
from dotenv import load_dotenv
from db import Database

load_dotenv()
db = Database(os.getenv('DATABASE_URL'))


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