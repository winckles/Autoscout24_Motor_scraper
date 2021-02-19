import psycopg2
import os


def connect_heroku():
    """ Connects to the heroku database """

    # connection = psycopg2.connect(os.environ['DATABASE_URL'])
    connection = psycopg2.connect('postgres://rcdpozbtfmhiqm:39011b4e67c734179fcb231dc2d4dd14de232097833134f5eff5ac02a6285d7b@ec2-54-198-73-79.compute-1.amazonaws.com:5432/dakf5mq8ckvgdo')

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
    """ Inserts a dataframe into the SQL tables in Heroku"""
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
    Selects 10 most recent requests and responses from the database
    :return: list of 10 most recent requests and responses from the database
    """
    connected = connect_heroku()
    cur = connected.cursor()

    cur.execute(f'''
            SELECT * FROM predictions ORDER BY id DESC LIMIT 10
            ''')

    return cur.fetchall()
