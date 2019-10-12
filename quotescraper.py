import re
import datetime
import sys
import json.decoder
import requests
from lxml import html
from datetime import datetime, timedelta



def make_request():
    response = requests.request('GET', 'https://bash.im/')
    parsed = html.fromstring(response.text)
    articles_from_html = parsed.xpath('//article[@class="quote"]')
    # ('//*[@id="departure-city"]/option[@value]/text()')
    
    input()


make_request()

