import psycopg2
import os


def connect_heroku():
    """
    Connects to the heroku database
    :return: connection
    """

    connection = psycopg2.connect(os.environ['DATABASE_URL'])

    return connection


def create_table():
    """ Create table 'predictions' in Heroku """
    connected = connect_heroku()
    cur = connected.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id serial PRIMARY KEY,
        inputs varchar(2000),
        outputs varchar(2000)
    );
    ''')

    connected.commit()


def insert_into_table(inputs, outputs):
    """ Inserts the predictions into the predictions table in Heroku"""
    connected = connect_heroku()
    cur = connected.cursor()

    cur.execute(f"""
    INSERT INTO predictions(inputs, outputs) 
    VALUES('{inputs}', '{outputs}');
    """)

    connected.commit()


def drop_table(table_name):
    """ Drop table with table_name in the heroku database """
    connected = connect_heroku()
    cur = connected.cursor()

    cur.execute(f'''
        DROP TABLE IF EXISTS {table_name} CASCADE
        ''')

    connected.commit()


def select_from_table() -> list:
    """
    Retrieves the last 10 records from the heroku database
    :return: 10 last records
    """
    connected = connect_heroku()
    cur = connected.cursor()

    cur.execute(f'''
            SELECT * FROM predictions ORDER BY id DESC LIMIT 10
            ''')

    return cur.fetchall()
