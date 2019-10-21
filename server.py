"""
The server.
"""
from flask import Flask, render_template, request, escape, session, copy_current_request_context, abort
from DBcm import DBfiller
from quotescraper import scrape_quotes_from_page
from threading import Thread


app = Flask(__name__)
quotes = scrape_quotes_from_page(1)


@app.route('/')
def entry_page() -> 'html':
    """Renders HTML-form"""
    return render_template('entry.html',
                           the_title='Welcome to Bash_quotes! ;)')


@app.route('/all_quotes')
def show_all_quotes():
    return render_template('viewallquotes.html',
                           the_title='ALL QUOTES FROM BASH IN SINGLE PLACE, AAAAA!!!!!')


@app.route('/all_quotes/scrape')
def fill_db_with_quotes():
    filler = DBfiller()
    filler.scrape_all_quotes()
    return render_template('quotes_are_scraped.html',
                           the_title="You're the most patient person! RESPECT!")


# @app.route('/quote<int:quote_id_on_html>')
@app.route('/quote')
# def show_quote_by_id(quote_id_on_html):
def show_quote_by_id():

    quote_id = request.args.get('quote_id_on_html', None)
    try:
        quote_id = int(quote_id)
    except Exception as err:
        quote_id = 1
    if quote_id < 1 or quote_id > 1000000:
        quote_id = 1
    print('quote_id = ', quote_id)

    try:
        selecter = DBfiller()
        finded_quote = selecter.select_quote_by_id(quote_id)
        return finded_quote
    except Exception as err:
        return 'No such quote.. Think about it.'

    return '<h1>Цитата из show_quote_by_id: <small>{}</small></h1>'.format(quote_id)
    # quote_to_show = [quote for quote in quotes if quote['id'] == quote_id]
    # if len(quote_to_show) == 1:
    #     result = '<h1>Цитата № {id}:</h1><p><b>{text}</h3></b><p>Дата: {date}</p><p>Рейтинг: {rating}</p>'
    #     result = result.format(**quote_to_show[0])
    #     return result
    # else:
    #     abort(404)

    # try:
    #     q_id = int(request.args.get('quote_id_on_html'))
    #     if q_id < 1 or q_id > 1000000:
    #         q_id = 1
    # except Exception:
    #     q_id = 1
    # return '<h1>Цитаты из show_quote_by_id: <small>{}</small></h1>'.format(q_id)


app.secret_key = 'DoItTryItYouWillNeverGuessIt'

if __name__ == '__main__':
    app.run(port=5010, debug=True)
