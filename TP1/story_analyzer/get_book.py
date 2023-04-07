import requests
from bs4 import BeautifulSoup, NavigableString

# TODO: need to check conditions, maybe use the other format
# Check if it is only accumulate <p></p> tags

def treat_html(html):
    text = ""
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('span', {'class': 'pagenum'})
    captions = soup.find_all('div', {'class': 'caption'})
    span_captions = soup.find_all('span', {'class': 'caption'})
    tocs = soup.find_all('p', {'class': 'toc'})
    blks = soup.find_all('div', {'class': 'blk'})
    h2s = soup.find_all('h2')
    figcenters = soup.find_all('div', {'class': 'figcenter'})
    anchors = soup.find_all('a')
    images = soup.find_all('img')
    pcs = soup.find_all('p', {'class': 'c'})
    tables = soup.find_all('table')
    for page in pages:
        page.extract()
    for caption in captions:
        caption.extract()
    for h2 in h2s:
        h2.extract()
    for span_caption in span_captions:
        span_caption.extract()
    for figcenter in figcenters:
        figcenter.extract()
    for anchor in anchors:
        anchor.extract()
    for blk in blks:
        blk.extract()
    for toc in tocs:
        toc.extract()
    for pc in pcs:
        pc.extract()
    for image in images:
        image.extract()
    for table in tables:
        table.extract()
    hr = soup.find('hr', {'class': 'full'})
    nested = []
    for tag in hr.find_all_next():
        if tag in nested:
            nested.remove(tag)
        elif tag.name == "hr":
            break
        elif isinstance(tag, NavigableString):
            text += tag
        else:
            nested_tags = [
                t for t in tag.descendants if t.name is not None]
            for x in nested_tags:
                nested.append(x)
            if tag not in nested:
                text += tag.get_text()
    return text

def get_book(mode,book_name):
    book_string = ''
    
    if mode == 'local':
        input_file = open(book_name, 'r')
        book_string = input_file.read()
        input_file.close
    elif mode == 'web':
        search_url = f"http://www.gutenberg.org/ebooks/search/?query={book_name}"
        response = requests.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            book_id = soup.find('li', {'class': 'booklink'}).find('a')['href'].split('/')[-1]
            book_html_url = f"http://www.gutenberg.org/files/{book_id}/{book_id}-h/{book_id}-h.htm"
            response = requests.get(book_html_url)
            if response.status_code == 200:
                book_string = treat_html(response.content)
            else:
                raise ValueError(f"unavailable html version of the book")
        else:
            raise ValueError(f"unavailable book: {book_name}")
    
    return book_string