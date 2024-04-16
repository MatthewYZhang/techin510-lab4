import requests
from bs4 import BeautifulSoup

stop = False

def get_data(URL='https://quotes.toscrape.com/page/1'):
    global stop
    res = requests.get(URL)
    if res.status_code != 200:
        stop = True
        return
    soup = BeautifulSoup(res.text, 'html.parser')
    quote_divs = soup.select('div.quote')
    if len(quote_divs) == 0:
        stop = True
        return
    for i in range(len(quote_divs)):
        quote_div = quote_divs[i]
        # print(quote_div)
        quote_selector = 'span.text'
        quote = quote_div.select_one(quote_selector).text
        author_selector = 'small.author'
        author = quote_div.select_one(author_selector).text
        author_link_selector = 'span'
        author_link = quote_div.select(author_link_selector)[1].select('a')[0]['href']
        tag_selector = 'a.tag'
        tags = [t.text for t in quote_div.select(tag_selector)]
        tags_links = [t['href'] for t in quote_div.select(tag_selector)]
        print(quote, author, tags, tags_links, author_link, sep='\n', end='\n\n')

page_num = 1

while not stop:
    page = f'https://quotes.toscrape.com/page/{page_num}'
    get_data(page)
    page_num += 1