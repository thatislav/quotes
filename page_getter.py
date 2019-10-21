"""
It gets number of pages.
"""
import requests
from lxml import html


def make_request():
    try:
        url = 'https://bash.im/'
        req = requests.request('GET', url)
        parsed = html.fromstring(req.text)
        return parsed
    except Exception as err:
        print('WARNING: some problems with"', url, '"')


def get_page_quantity(response):
    pages = response.xpath('string(//main/div/input[@type="number"][@class="pager__input"]/@max)')
    return pages


def count_pages():
    response = make_request()
    pages_quantity = int(get_page_quantity(response))
    return pages_quantity


# count_pages()
