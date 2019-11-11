from data_layer.connections import get_connection
from data_layer.schema import setup_trade_table


if __name__ == "__main__":
    setup_trade_table(get_connection())
