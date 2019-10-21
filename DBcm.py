"""
Instrument for connection to the DataBase.
Adds all quotes to DataBase.
"""
from quotescraper import scrape_quotes_from_page
from page_getter import count_pages
import sqlite3


pages = count_pages()
conn = sqlite3.connect('QuotesDB.db')
cur = conn.cursor()


def create_table_quotes():
    try:
        _SQL_create_table_quotes = """CREATE TABLE QUOTES
                                    ([quote_id] integer PRIMARY KEY,
                                    [quote_date] date,
                                    [quote_text] text,
                                    [quote_rate] integer)
                                """
        cur.execute(_SQL_create_table_quotes)
        conn.commit()
    except sqlite3.OperationalError as err:
        print('\nWARNING: Trying to create table QUOTES, getting:\n"', err, '"')


def scrape_all_quotes(pages_quantity):
    for page_number in range(1, pages_quantity+1):
        quotes_from_single_page = scrape_quotes_from_page(page_number)
        add_quotes_to_db(quotes_from_single_page)


def add_quotes_to_db(quotes):
    # existing_ids = 0
    for quote in quotes:
        _SQL_insert_quotes = """INSERT INTO QUOTES 
                                (quote_id, quote_date, quote_text, quote_rate)
                                VALUES
                                ({id}, '{date}', '{text}', {rating})
                            """.format(**quote)
        try:
            cur.execute(_SQL_insert_quotes)
        except Exception as err:
            continue
    conn.commit()
    #         existing_ids += 1
    # if existing_ids > 0:
    #     print('\nWARNING:', existing_ids, 'quotes we just trying to add are already exists.\n')


def count_quotes_in_db():
    _SQL_select_quotes = """
                            --SELECT quote_id, quote_date, '', '', ''
                            --FROM QUOTES
                            --WHERE date(quote_date) = '2019-10-20'
                            --UNION
                            SELECT '','','====================', 'QUOTES TOTAL in DB: ', count(quote_id)
                            FROM QUOTES
                        """
    try:
        cur.execute(_SQL_select_quotes)
        for item in cur.fetchall():
            for i in item:
                print(i)
    except Exception as err:
        print('\nWARNING: Something went wrong in "select_quotes":\n"', err, '"')


def mainer():
    create_table_quotes()
    scrape_all_quotes(pages)
    # count_quotes_in_db()


# mainer()

conn.close()


class UseDatabase:

    def __init__(self, config: dict) -> None:
        self.configuration = config

    def __enter__(self) -> 'cursor':
        try:
            self.conn = sqlite3.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except Exception as err:
            raise err
        # except mysql.connector.errors.InterfaceError as err:
        #     raise ConnectionError(err)
        # except mysql.connector.errors.ProgrammingError as err:
        #     raise CredentialsError(err)

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        # if exc_type is mysql.connector.errors.ProgrammingError:
        #     raise SQLError(exc_value)
        # elif exc_type:
        #     raise exc_type(exc_value)
