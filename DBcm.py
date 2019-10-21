"""
Instrument for connection to the DataBase.
Adds all quotes to DataBase.
"""
from quotescraper import scrape_quotes_from_page
from page_getter import count_pages
import sqlite3


class DBfiller:

    def __init__(self):
        self.pages = count_pages()
        self.conn = sqlite3.connect('QuotesDB.db')
        self.cur = self.conn.cursor()
        self.create_table_quotes()

    def create_table_quotes(self):
        try:
            _SQL_create_table_quotes = """CREATE TABLE QUOTES
                                        ([quote_id] integer PRIMARY KEY,
                                        [quote_date] date,
                                        [quote_text] text,
                                        [quote_rate] integer)
                                    """
            self.cur.execute(_SQL_create_table_quotes)
            self.conn.commit()
        except sqlite3.OperationalError as err:
            print('\nWARNING: Trying to create table QUOTES, getting:\n"', err, '"')

    def scrape_all_quotes(self):
        for page_number in range(1, self.pages+1):
            quotes_from_single_page = scrape_quotes_from_page(page_number)
            self.add_quotes_to_db(quotes_from_single_page)

    def add_quotes_to_db(self, quotes):
        # existing_ids = 0
        for quote in quotes:
            _SQL_insert_quotes = """INSERT INTO QUOTES 
                                    (quote_id, quote_date, quote_text, quote_rate)
                                    VALUES
                                    ({id}, '{date}', '{text}', {rating})
                                """.format(**quote)
            try:
                self.cur.execute(_SQL_insert_quotes)
            except Exception as err:
                continue
        self.conn.commit()
        #         existing_ids += 1
        # if existing_ids > 0:
        #     print('\nWARNING:', existing_ids, 'quotes we just trying to add are already exists.\n')

    def count_quotes_in_db(self):
        _SQL_select_quotes = """
                                --SELECT quote_id, quote_date, '', '', ''
                                --FROM QUOTES
                                --WHERE date(quote_date) = '2019-10-20'
                                --UNION
                                SELECT '','','====================', 'QUOTES TOTAL in DB: ', count(quote_id)
                                FROM QUOTES
                            """
        try:
            self.cur.execute(_SQL_select_quotes)
            for item in self.cur.fetchall():
                for i in item:
                    print(i)
        except Exception as err:
            print('\nWARNING: Something went wrong in "select_quotes":\n"', err, '"')

    def select_quote_by_id(self, id):
        _SQL_select_quote_by_id = """SELECT *
                                    FROM QUOTES
                                    WHERE quote_id = {}""".format(id)
        try:
            self.cur.execute(_SQL_select_quote_by_id)
            for item in self.cur.fetchall():
                for i in item:
                    print(i)
            acceptable_form_for_flask = tuple(self.cur.fetchall())
            return acceptable_form_for_flask
        except Exception as err:
            print('\nWARNING: Something went wrong in "select_quote_by_id":\n"', err, '"')

    def finish_work(self):
        self.conn.close()

    # def quotes_miner():
    #     create_table_quotes()
    #     scrape_all_quotes(pages)
        # count_quotes_in_db()


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
