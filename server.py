"""
The server.
"""
from flask import Flask, render_template, request, escape, session, copy_current_request_context, abort
from DBcm import UseDatabase
from quotescraper import scrape_quotes_from_page
from threading import Thread


app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'quot',
                          'password': 'quotpassquord',
                          'database': 'quoteslogDB', }

quotes = scrape_quotes_from_page()
quote_ids = [quote['id'] for quote in quotes]

@app.route('/')
def entry_page() -> 'html':
    """Renders HTML-form"""
    return render_template('entry.html',
                           the_title='Welcome to Bash_quotes!')


@app.route('/quotes')
def show_all_quotes():
    try:
        q_id = int(request.args.get('id'))
        if q_id < 1 or q_id > 1000000:
            q_id = 1
    except Exception:
        q_id = 1
    return '<h1>Цитаты: <small>{}</small></h1>'.format(q_id)


@app.route('/quotes/<int:quote_id>')
def show_quote_by_id(quote_id):
    quote_to_show = [quote for quote in quotes if quote['id'] == quote_id]
    if len(quote_to_show) == 1:
        result = '<h1>Цитата № {id}:</h1><p><b>{text}</h3></b><p>Дата: {date}</p><p>Рейтинг: {rating}</p>'
        result = result.format(**quote_to_show[0])
        return result
    else:
        abort(404)


app.secret_key = 'DoItTryItYouWillNeverGuessIt'

if __name__ == '__main__':
    app.run(port=5010, debug=True)
