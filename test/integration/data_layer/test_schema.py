import unittest
from data_layer.schema import Trade, setup_trade_table, delete_trade_table
from data_layer.connections import get_connection

import mock


class Test_Trade(unittest.TestCase):

    def setUp(self):
        self.connection = get_connection(False, "test.db")

        # Clear and setup tables between tests
        delete_trade_table(self.connection)
        setup_trade_table(self.connection)

    def tearDown(self):
        # Clean up test database between tests
        delete_trade_table(self.connection)

    @mock.patch("time.time")
    def test_save(self, mocked_time):
        mocked_time.return_value = 10000.0
        fields = ["sell_currency", "sell_amount", "buy_currency", "buy_amount", "rate"]
        values = ["GBP", 100.0, "USD", 140.0, 1.4]
        trade = Trade(connection=self.connection, **dict(zip(fields, values)))
        trade.save()
        trades = list(trade.fetch_all(connection=self.connection))
        self.assertEqual(len(trades), 1)
        self.assertEqual(values + [10000.0], trades[0].values())


if __name__ == "__main__":
    unittest.main()