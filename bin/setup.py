from data_layer.schema import TRADE_TABLE_SCHEMA
from data_layer.connections import get_connection
import sqlite3


def setup_trade_table(connection):
    """
    Setups the sqlite3 tables, does nothing if the table already exists

    :param sqlite3.Connection connection: the connection to setup the table structure for
    """
    cursor = connection.cursor()

    try:
        cursor.execute(TRADE_TABLE_SCHEMA)
    except sqlite3.OperationalError:
        print("Table Already Exists!")
        return

    connection.commit()
    connection.close()


if __name__ == "__main__":
    setup_trade_table(get_connection())
