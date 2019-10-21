"""
The scraper.
It scrapes quotes from single page.
"""
import re
import datetime
import sys
import json.decoder
import requests
from lxml import html
from datetime import datetime, timedelta
from itertools import groupby


def make_request(page) -> 'HtmlElement':
    """- One request, please."""
    try:
        url = 'https://bash.im/index/{}'.format(page)
        response = requests.request('GET', url)
        parsed = html.fromstring(response.text)
        return parsed
    except Exception as err:
        print('\nWARNING: problems with"', url, '".\n###', err)
        return None


def get_all_articles_from_page(parsed) -> list:
    """- Where is my quotes, I said!!!???"""
    try:
        articles_from_html = parsed.xpath('//article[@class="quote"]')
        articles_ready = []
        for article_raw in articles_from_html:
            article_ready = get_article(article_raw)
            articles_ready.append(article_ready)
        return articles_ready
    except Exception as err:
        print('\nWARNING: problems with getting articles from page.\n###', err)
        return None


def get_article(article_from_html) -> dict:
    """Let's clean the dirty one."""
    quote_id = int(article_from_html.xpath('string(.//@data-quote)'))
    quote_datetime = clean_quote_date(article_from_html)
    quote_text = clean_quote_text(article_from_html)
    quote_rating = clean_quote_rating(article_from_html)
    article = {'id': quote_id,
               'date': quote_datetime,
               'text': quote_text,
               'rating': quote_rating
               }
    return article


def clean_quote_date(article_from_html) -> datetime:
    """I like clean dates,"""
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


def clean_quote_text(article_from_html) -> str:
    """..and pure text,"""
    raw_body = article_from_html.xpath('.//div[@class="quote__body"]/text()')
    raw_text = '\n'.join(raw_body)
    pure_text = raw_text.strip()
    return pure_text


def clean_quote_rating(article_from_html) -> int:
    """..and of course pure rating in my quotes."""
    raw_rating = article_from_html.xpath('.//div[@class="quote__total"]/text()')
    try:
        pure_rating = int(raw_rating[0])
    except ValueError:
        pure_rating = 0
    return pure_rating


def scrape_quotes_from_page(page):
    """Let's rock and get some quotes."""
    parsed = make_request(page)
    articles = get_all_articles_from_page(parsed)
    return articles
