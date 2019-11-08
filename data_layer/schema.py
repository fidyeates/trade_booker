"""
data_layer.schema

Handles functionality around database schema objects and standardised methods for persistance and loading.
"""
from data_layer.connections import get_connection
import string
import time

CHARACTERS = string.ascii_letters + string.digits

MAX_ID = 62 ** 7


def id_to_string(id):
    """
    Converts an integer id into the specified index format: TR + 7 alphanumeric characters

    Would prefer to do this within the Trade __init__ method, or within the database itself.

    Note: This setup only supports ID's of values in the range 0 to (62 ** 7) - 1, while not a small number having
    a good partition key will be essential in spreading the load over different database shares with high volume datasets.

    :param int id: The auto-incrementing integer id for the Trade
    :rtype: str
    """
    if id < 0 or id >= MAX_ID:
        raise OverflowError("Trade ID is out of range")
    output = []
    for i in range(7):
        this_index = int(id % 62)
        id = int(id / 62)
        output.append(CHARACTERS[this_index])
    return "TR" + "".join(output[::-1])


def validate_input(value, types):
    """
    Validates that the input argument matches the correct type

    :param value: The value to check
    :param type: The required type class for value validation
    """
    if not isinstance(value, types):
        raise TypeError(f"Value: {value!r}, got type {type(value)} expected type: {types}")
    return value


class Trade(object):

    TABLE_NAME = "trades"
    FIELDS = ["sell_currency", "sell_amount", "buy_currency", "buy_amount", "rate", "date_booked"]
    TYPES = dict(zip(FIELDS, [str, (float, int), str, (float, int), (float, int), float]))

    def __init__(self, connection=None, **kwargs):
        """
        The Trade object contains encapsulated functionality to save and load trades from the sqlite3 database.

        :param sqlite3.Connection connection: A sqlite3 connection object
        :param int id: The unique id for this trade
        :param str sell_currency: The sell currency
        :param float sell_amount: The amount of currency sold
        :param str buy_currency: The buy currency
        :param float buy_amount: The amount of currency bought
        :param float rate: The conversion rate used
        :param float date_booked: The timestamp of time of creation of the trade
        """
        if not connection:
            connection = get_connection()
        self.connection = connection

        # Variables
        self.id = kwargs.get("id", None)
        self.sell_currency = validate_input(kwargs["sell_currency"], self.TYPES["sell_currency"])
        self.sell_amount = validate_input(kwargs["sell_amount"], self.TYPES["sell_amount"])
        self.buy_currency = validate_input(kwargs["buy_currency"], self.TYPES["buy_currency"])
        self.buy_amount = validate_input(kwargs["buy_amount"], self.TYPES["buy_amount"])
        self.rate = validate_input(kwargs["rate"], self.TYPES["rate"])
        self.date_booked = validate_input(kwargs.get("date_booked", time.time()), self.TYPES["date_booked"])

    def __repr__(self):
        param_string = [f"{attr}={getattr(self, attr)!r}" for attr in ["id"] + self.FIELDS]
        return f"Trade({', '.join(param_string)})"

    def save(self):
        """
        Persists this Trade in the sqlite3 database
        """
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO {self.TABLE_NAME}(sell_currency, sell_amount, buy_currency, buy_amount, rate, date_booked) VALUES (?, ?, ?, ?, ?, ?)", self.values())
        self.connection.commit()

    def values(self):
        """
        Returns an ordered list of this Trades parameters, useful for saving state in the database.
        :rtype: list
        """
        return [getattr(self, attr) for attr in self.FIELDS]

    @staticmethod
    def fetch_all(connection=None):
        """
        Returns a generator over all available Trades in the database in order from the most recent created to the oldest
        created.

        :param sqlite3.Connection connection: A sqlite3 connection object
        :rtype: Generator[Trade]
        """
        if connection is None:
            connection = get_connection()
        cursor = connection.cursor()
        for raw in cursor.execute(f"SELECT * FROM {Trade.TABLE_NAME} ORDER BY date_booked DESC"):
            yield Trade(**dict(zip(["id"] + Trade.FIELDS, raw)))

    def format_date(self):
        """
        Formats the timestamp as a human readable date for display purposes
        :rtype: str
        """
        return time.strftime("%d/%m/%Y %H:%M", time.localtime(self.date_booked))

    def format_id(self):
        """
        Formats the unique integer id as a human readable format
        :rtype: str
        """
        return id_to_string(self.id)


TRADE_TABLE_SCHEMA = """CREATE TABLE {} 
    (
        id integer primary key, 
        sell_currency text, 
        sell_amount real,
        buy_currency text,
        buy_amount real,
        rate real,
        date_booked real
    )
""".format(Trade.TABLE_NAME)
