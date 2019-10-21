"""
It gets number of pages.
"""
import requests
from lxml import html


def make_request():
    """Request of course."""
    try:
        url = 'https://bash.im/'
        req = requests.request('GET', url)
        parsed = html.fromstring(req.text)
        return parsed
    except Exception as err:
        print('\nWARNING: problems with"', url, '".\n###', err)
        return None


def get_page_quantity(response):
    """So let's find this little attribute with pages number."""
    try:
        pages = response.xpath('string(//main/div/input[@type="number"][@class="pager__input"]/@max)')
        return pages
    except Exception as err:
        print('\nWARNING: problems with getting number of pages.\n###', err)
        return 0


def count_pages():
    """Main func."""
    response = make_request()
    pages_quantity = int(get_page_quantity(response))
    return pages_quantity
