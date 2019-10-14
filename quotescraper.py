import re
import datetime
import sys
import json.decoder
import requests
from lxml import html
from datetime import datetime, timedelta
from itertools import groupby


def make_request():
    response = requests.request('GET', 'https://bash.im/')
    parsed = html.fromstring(response.text)
    # ('//*[@id="departure-city"]/option[@value]/text()')
    return parsed


def get_all_articles_from_page(parsed):
    articles_from_html = parsed.xpath('//article[@class="quote"]')
    articles_ready = []
    for ar in articles_from_html:
        article_ready = get_article(ar)
        articles_ready.append(article_ready)
    return articles_ready


def get_article(article_from_html):
    quote_id = int(article_from_html.xpath('string(.//@data-quote)'))
    quote_datetime = clean_quote_date(article_from_html)
    quote_text = clean_quote_text(article_from_html)
    quote_rating = clean_quote_rating(article_from_html)
    article = {'id': quote_id,
               'date': quote_datetime,
               'body': quote_text,
               'rating': quote_rating
               }
    return article


def clean_quote_date(article_from_html):
    raw_date = article_from_html.xpath('.//div[@class="quote__header_date"]/text()')
    date_pre = str(raw_date[0])
    first_level = re.findall(r'(\d{1,2}\.\d{1,2}\.\d{4})|(\d{1,2}\:\d{2})', date_pre)
    second_level = []
    for snippet in first_level:
        for chunk in snippet:
            second_level.append(chunk) if chunk else None
    pure_date_str = ' '.join(second_level)
    if pure_date_str[-5] == ' ':
        pure_date_str = pure_date_str[:-4] + '0' + pure_date_str[-4:]
    pure_date = datetime.strptime(pure_date_str, '%d.%m.%Y %H:%M')
    return pure_date


def clean_quote_text(article_from_html):
    raw_body = article_from_html.xpath('.//div[@class="quote__body"]/text()')
    pure_text = str(raw_body[0]).strip()
    return pure_text


def clean_quote_rating(article_from_html):
    raw_rating = article_from_html.xpath('.//div[@class="quote__total"]/text()')
    try:
        pure_rating = int(raw_rating[0])
    except ValueError:
        pure_rating = 0
    return pure_rating


def master_def():
    parsed = make_request()
    articles = get_all_articles_from_page(parsed)
    return articles


master_def()