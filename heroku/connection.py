import psycopg2
import os


def connect_heroku():
    """ Connects to the heroku database """

    connection = psycopg2.connect(
        database=os.environ['DATABASE'],
        user=os.environ['USER'],
        password=os.environ['PASSWORD'],
        host=os.environ['HOST'],
        port=os.environ['PORT'],
    )

    return connection
