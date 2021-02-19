import psycopg2
import os


def connect_heroku():
    """ Connects to the heroku database """

    connection = psycopg2.connect(
        database=os.getenv('DATABASE'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        host=os.getenv('HOST'),
        port=os.getenv('PORT')
    )

    return connection
