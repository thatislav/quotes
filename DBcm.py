"""
Instrument for connection to the DataBase.
"""
import sqlite3
from quotescraper import scrape

quotes = scrape()
quote_ids = [quote['id'] for quote in quotes]

conn = sqlite3.connect('QuotesDB.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE QUOTES
(
[quote_id] integer,
[quote_date] date,
[quote_text] text,
[quote_rate] integer)
""")

for quote in quotes:
    cur.execute("""
    INSERT INTO QUOTES VALUES
    ({id}, {date}, '{text}', {rating})
    """.format(**quote))

conn.commit()

cur.execute("""
SELECT * FROM QUOTES
""")
for item in cur.fetchall():
    for i in item:
        print(i)

conn.close()


class ConnectionErr(Exception):
    pass


class CredentialsErr(Exception):
    pass


class SQLError(Exception):
    pass


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
