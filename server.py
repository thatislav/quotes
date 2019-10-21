"""
The server.
"""
from flask import Flask, render_template, request, escape, session, copy_current_request_context, abort
# from DBcm import UseDatabase
from quotescraper import scrape_quotes_from_page
from threading import Thread


app = Flask(__name__)
quotes = scrape_quotes_from_page(1)


@app.route('/')
def entry_page() -> 'html':
    """Renders HTML-form"""
    return render_template('entry.html',
                           the_title='Welcome to Bash_quotes!')


@app.route('/all_quotes')
def show_all_quotes():
    return render_template('viewallquotes.html',
                           the_title='ВСЕ ЦИТАТЫ С БАША В ОДНОМ МЕСТЕ, ААААА!!!!!')


@app.route('/quote/<int:quote_id_on_html>')
def show_quote_by_id(quote_id_on_html):

    quote_id_from_form = request.values.get('quote_id_on_html')
    if quote_id_from_form < 1 or quote_id_from_form > 1000000:
        quote_id_from_form = 1

    return '<h1>Цитаты из show_quote_by_id: <small>{}</small></h1>'.format(quote_id_from_form)
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
