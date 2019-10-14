import re
import datetime
import sys
import json.decoder
import requests
from lxml import html
from datetime import datetime, timedelta
from itertools import groupby


article = {'id': '',
           'date': '',
           'body': '',
           'rating': ''
           }


def make_request():
    response = requests.request('GET', 'https://bash.im/')
    parsed = html.fromstring(response.text)
    # ('//*[@id="departure-city"]/option[@value]/text()')
    return parsed


def get_articles_from_page(parsed):
    articles_from_html = parsed.xpath('//article[@class="quote"]')
    articles_ready = []
    for ar in articles_from_html:
        article_ready = get_article(ar)
        articles_ready.append(article_ready)
    return articles_ready


def get_article(article_from_html, *args, **kwargs):
    id = article_from_html.xpath('string(//@data-quote)')
    raw_date = article_from_html.xpath('.//div[@class="quote__header_date"]/text()')
    datetime_act = raw_date[0].split('в')
    datetime_act_1 = [part.strip() for part in datetime_act]
    datetime_sec = clean_date(raw_date)
    datetime_third = str(raw_date[0]).replace('в', '').strip()
    input()


def clean_date(raw_date):
    test = str(raw_date[0])
    first_level = re.findall(r'(\d{1,2}\.\d{1,2}\.\d{4})|(\d{1,2}\:\d{2})', test)
    second_level = []
    for snippet in first_level:
        for chunk in snippet:
            second_level.append(chunk) if chunk else None
    pure_date_str = ' '.join(second_level)
    if pure_date_str[-5] == ' ':
        pure_date_str = pure_date_str[:-4] + '0' + pure_date_str[-4:]
    pure_date = datetime.strptime(pure_date_str, '%d.%m.%Y %H:%M')
    return pure_date


def master_def():
    parsed = make_request()
    articles = get_articles_from_page(parsed)


master_def()