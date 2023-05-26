import json
import requests
from bs4 import BeautifulSoup


def get_quote_data(quote):
    text = quote.find('span', class_='text').text
    author = quote.find('small', class_='author').text
    tags = [tag.text for tag in quote.find_all('a', class_='tag')]
    return {
        'tags': tags,
        'author': author,
        'quote': text,
    }


def get_author_data(author_url): # noqa
    response = requests.get(author_url) # noqa
    soup = BeautifulSoup(response.text, 'html.parser') # noqa
    author_name = soup.find('h3', class_='author-title').text.strip().split("\n")[0]
    author_born_date = soup.find('span', class_='author-born-date').text.strip()
    author_born_location = soup.find('span', class_='author-born-location').text.strip()
    author_description = soup.find('div', class_='author-description').text.strip()
    return {
        'fullname': author_name,
        'born_date': author_born_date,
        'born_location': author_born_location,
        'description': author_description
    }


page_number = 1
quotes = []
authors = []

while True:
    url = f'http://quotes.toscrape.com/page/{page_number}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quote_elements = soup.find_all('div', class_='quote')
    if len(quote_elements) == 0:
        break

    for quote_element in quote_elements:
        quote_data = get_quote_data(quote_element)
        quotes.append(quote_data)

        author_url = quote_element.find('a')['href']
        author_data = get_author_data(f'http://quotes.toscrape.com{author_url}')
        authors.append(author_data)

    page_number += 1

with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
    json.dump(quotes, quotes_file, indent=4, ensure_ascii=False)

with open('authors.json', 'w', encoding='utf-8') as authors_file:
    json.dump(authors, authors_file, indent=4, ensure_ascii=False)
