"""
Instrument for connection to the DataBase.
Performs all operations with quotes within DataBase.
"""
from quotescraper import scrape_quotes_from_page
from page_getter import count_pages
import sqlite3


class DBfiller:
    """Whole work between quotes and DataBase performs via this guy."""

    def __init__(self, scrape_all_quotes=False):
        """Starts scraping quotes and filling DB by itself if 'scrape_all_quotes' is True.
        So be carefull."""
        self.pages = count_pages()
        self.conn = sqlite3.connect('QuotesDB.db')
        self.cur = self.conn.cursor()
        if scrape_all_quotes:
            self.create_table_quotes()
            self.scrape_all_quotes()
            self.finish_work()

    def create_table_quotes(self):
        """Creates empty table for further work."""
        _SQL_create_table_quotes = """CREATE TABLE QUOTES
                                    ([quote_id] integer PRIMARY KEY,
                                    [quote_date] date,
                                    [quote_text] text,
                                    [quote_rate] integer)
                                """
        try:
            self.cur.execute(_SQL_create_table_quotes)
            self.conn.commit()
        except sqlite3.OperationalError as err:
            print('\nWARNING: Trying to create table QUOTES, problems:\n###', err)
        except Exception as err:
            print('\nWARNING: other problems when creating table QUOTES:\n###', err)

    def scrape_all_quotes(self):
        """Scrapes quotes from all pages. It costs about 40 minutes. I tried."""
        for page_number in range(1, self.pages+1):
            try:
                quotes_from_single_page = scrape_quotes_from_page(page_number)
                self.add_quotes_to_db(quotes_from_single_page)
            except Exception as err:
                print('\nWARNING: problems with adding quotes from page to DB.\n###', err)
                break

    def add_quotes_to_db(self, quotes):
        """Adds quotes scraped from one page to DB."""
        _SQL_insert_quotes = """INSERT INTO QUOTES 
                                (quote_id, quote_date, quote_text, quote_rate)
                                VALUES
                                ({id}, '{date}', '{text}', {rating})
                            """
        for quote in quotes:
            try:
                self.cur.execute(_SQL_insert_quotes.format(**quote))
            except Exception:
                continue
        self.conn.commit()

    def count_quotes_in_db(self):
        """Sometimes I will add this counter to site."""
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
            print('\nWARNING: problems in "select_quotes":\n###', err)

    def select_quote_by_id(self, qq_id):
        """Selects quote you wanted."""
        _SQL_select_quote_by_id = """SELECT *
                                    FROM QUOTES
                                    WHERE quote_id = {}""".format(qq_id)
        try:
            self.cur.execute(_SQL_select_quote_by_id)
            data_quote_by_id = self.cur.fetchall()
            return data_quote_by_id
        except Exception as err:
            print('\nWARNING: problems in "select_quote_by_id":\n###', err)

    def finish_work(self):
        """Closes connection. Implemented badly, I know."""
        self.conn.close()
