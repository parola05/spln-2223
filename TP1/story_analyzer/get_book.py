import requests
import re
from bs4 import BeautifulSoup, NavigableString


def decompose_tag(tags):
    for tag in tags:
        tag.decompose()


def remove_useless_tags(soup):
    decompose_tag(soup.find_all('head'))
    decompose_tag(soup.find_all('div', {'class': 'footnote'}))
    decompose_tag(soup.find_all('div', {'class': 'footnotes'}))
    decompose_tag(soup.find_all('hr'))
    decompose_tag(soup.find_all('span', {'class': 'pagenum'}))
    decompose_tag(soup.find_all('div', {'class': 'caption'}))
    decompose_tag(soup.find_all('span', {'class': 'caption'}))
    decompose_tag(soup.find_all('div', {'class': 'toc'}))
    decompose_tag(soup.find_all('p', {'class': 'toc'}))
    decompose_tag(soup.find_all('div', {'class': 'blk'}))
    decompose_tag(soup.find_all('h1'))
    decompose_tag(soup.find_all('section'))
    decompose_tag(soup.find_all('div', {'class': 'dedication'}))
    decompose_tag(soup.find_all('div', {'class': 'epigraph'}))
    decompose_tag(soup.find_all('h2'))
    decompose_tag(soup.find_all('div', {'class': 'figcenter'}))
    decompose_tag(soup.find_all('a'))
    decompose_tag(soup.find_all('img'))
    decompose_tag(soup.find_all('p', {'class': 'c'}))
    decompose_tag(soup.find_all('table'))
    decompose_tag(soup.find_all('div', style=True))
    return soup


def treat_html(html):
    result = ""
    soup = remove_useless_tags(BeautifulSoup(html, 'html.parser'))
    nested = []
    for tag in soup.find_all():
        if tag in nested:
            nested.remove(tag)
        elif isinstance(tag, NavigableString):
            result += tag
        else:
            nested_tags = [
                t for t in tag.descendants if t.name is not None]
            for x in nested_tags:
                nested.append(x)
            if tag not in nested:
                result += tag.get_text()
    return result


def trim_newlines(text):
    return re.sub(r'\s*\n\s*', '\n', text)


def get_book(mode, book_name):
    book_string = ''

    if mode == 'local':
        input_file = open(book_name, 'r')
        book_string = input_file.read()
        input_file.close()
    elif mode == 'web':
        search_url = f"http://www.gutenberg.org/ebooks/search/?query={book_name}"
        response = requests.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            book_id = soup.find('li', {'class': 'booklink'}).find('a')[
                'href'].split('/')[-1]
            book_html_url = f"http://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}-images.html"
            response = requests.get(book_html_url)
            if response.status_code == 200:
                book_string = trim_newlines(treat_html(response.content))
            else:
                raise ValueError(f"unavailable html version of the book")
        else:
            raise ValueError(f"unavailable book: {book_name}")

    return book_string
