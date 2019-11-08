import sqlite3

CONNECTION = None
DATABASE_NAME = "trades.db"


def new_connection():
    """
    Gets a new connection for the sqlite3 database
    :rtype: sqlite3.Connection
    """
    return sqlite3.connect(DATABASE_NAME)


def get_connection(use_singleton=True, db_name=DATABASE_NAME):
    """
    Gets a connection to the database at the provided path.

    :param bool use_singleton: Should we return a singleton connection or generate a new one
    :param str db_name: The database path to connect to
    :rtype: sqlite3.Connection
    """
    global CONNECTION
    if use_singleton:
        if CONNECTION is None:
            CONNECTION = sqlite3.connect(db_name)
        return CONNECTION
    return sqlite3.connect(db_name)
