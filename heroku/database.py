import psycopg2
import os


def connect_heroku():
    """ Connects to the heroku database """

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


def insert_into_table(dataframe, keywords):
    """ Inserts a dataframe into the SQL tables in Heroku"""
    connected = connect_heroku()
    cur = connected.cursor()

    cur.execute(f"""
    INSERT INTO predictions(inputs, outputs) 
    VALUES('{keywords[0]}'), ('{keywords[1]}'), ('{keywords[2]}');
    """)

    for i, [index, row] in enumerate(dataframe.iterrows(), 1):
        cur.execute('''
        INSERT INTO products (id, title, price, itemUrl, imageUrl, category)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (i, row.title, row.price, row.url_to_item, row.url_to_image, row.category))

    connected.commit()


def drop_table( table_name):
    """ Drop table with table_name in the heroku database """
    connected = connect_heroku()
    cur = connected.cursor()

    cur.execute(f'''
        DROP TABLE IF EXISTS {table_name} CASCADE
        ''')

    connected.commit()


# def insert_in_table(input_request: str, output_response: str) -> None:
#     """
#     Inserts request and response into the database
#     :param input_request: request sent by the client (inputs)
#     :param output_response: response given by the server (predictions)
#     :return: None
#     """
#     try:
#         conn = get_connection()
#
#         if conn is not None:
#             cursor = conn.cursor()
#             cursor.execute(
#                 f"INSERT INTO lr (requests, responses) values ('{input_request}', '{output_response}')"
#             )
#             conn.commit()
#
#     except DatabaseError as err:
#         log_psycopg2_exception(err)
#
#
# def select_from_table() -> list:
#     """
#     Selects 10 most recent requests and responses from the database
#     :return: list of 10 most recent requests and responses from the database
#     """
#     try:
#         conn = get_connection()
#
#         if conn is not None:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM lr ORDER BY id DESC LIMIT 10")
#             return cursor.fetchall()
#
#     except DatabaseError as err:
#         log_psycopg2_exception(err)