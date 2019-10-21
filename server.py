"""
The server.
"""
from flask import Flask, render_template, request, escape, session, copy_current_request_context, abort
from DBcm import DBfiller
from quotescraper import scrape_quotes_from_page
from threading import Thread


app = Flask(__name__)
quotes = scrape_quotes_from_page(1) ###FIXME: for testing scrape only 1 page


@app.route('/')
def entry_page() -> 'html':
    """Renders homepage HTML-form"""
    return render_template('entry.html',
                           the_title='Welcome to Bash_quotes! ;)')


@app.route('/all_quotes')
def show_all_quotes():
    """Page where you can start the looongest action of your life."""
    return render_template('viewallquotes.html',
                           the_title='ALL QUOTES FROM BASH IN SINGLE PLACE, AAAAA!!!!!')


@app.route('/all_quotes/scrape')
def fill_db_with_quotes():
    """It's all your fault, as far as waiting. You've been warned)))"""
    DBfiller(scrape_all_quotes=True)
    return render_template('quotes_are_scraped.html',
                           the_title="You're the most patient person! RESPECT!")


@app.route('/quote')
def show_quote_by_id():
    """Cool feature. Just checkitout."""
    quote_id = request.args.get('quote_id_on_html', None)
    try:
        quote_id = int(quote_id)
    except Exception:
        quote_id = 1
    if quote_id < 1 or quote_id > 1000000:
        quote_id = 1
    print('quote_id =', quote_id)

    try:
        selector = DBfiller()
        finded_quote = selector.select_quote_by_id(quote_id)
        titles = ('###', 'Дата публикации', 'Цитата', 'Рейтинг')
        no_rezults = ('Yет', 'такой', 'цитаты,', 'Уважаемый')
        result = titles if finded_quote else no_rezults
        return render_template('quote_by_id.html',
                               the_title="Finded quote or quotes are all here.",
                               the_row_titles=result,
                               the_quotes=finded_quote)
    except Exception as err:
        print('\nWARNING: problems when search quote by id.###', err)
        entry_page()


app.secret_key = 'DoItTryItYouWillNeverGuessIt'

if __name__ == '__main__':
    app.run(port=5010, debug=True)
