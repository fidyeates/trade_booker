import unittest
from data_layer.schema import id_to_string, Trade, validate_input
import mock


class Test_id_to_string(unittest.TestCase):

    def test_simple_case(self):
        id = 1
        self.assertEqual(id_to_string(id), "TRaaaaaab")

    def test_simple_case_2(self):
        id = 0
        self.assertEqual(id_to_string(id), "TRaaaaaaa")

    def test_simple_case_3(self):
        id = 63
        self.assertEqual(id_to_string(id), "TRaaaaabb")

    def test_simple_case_4(self):
        id = 127531
        self.assertEqual(id_to_string(id), "TRaaaaHk7")

    def test_boundary_case_1(self):
        id = 62 ** 7 - 1
        self.assertEqual(id_to_string(id), "TR9999999")

    def test_error_case_1(self):
        id = 62 ** 7
        self.assertRaises(OverflowError, id_to_string, id)

    def test_error_case_2(self):
        id = -1
        self.assertRaises(OverflowError, id_to_string, id)

    def test_error_case_3(self):
        id = None
        self.assertRaises(TypeError, id_to_string, id)

    def test_error_case_4(self):
        id = "None"
        self.assertRaises(TypeError, id_to_string, id)


class Test_validate_input(unittest.TestCase):

    def test_string_validation_pass(self):
        input = "test_string"
        self.assertEqual(validate_input(input, str), input)

    def test_string_validation_fails(self):
        inputs = [None, 1, 1.0]
        for input in inputs:
            self.assertRaises(TypeError, validate_input, input, str)

    def test_number_validation_fails(self):
        inputs = [None, "1", "test"]
        for input in inputs:
            self.assertRaises(TypeError, validate_input, input, (int, float))

    def test_number_validation_pass(self):
        inputs = [0, -5, 10.25]
        for input in inputs:
            self.assertEqual(validate_input(input, (int, float)), input)


class Test_Trade(unittest.TestCase):

    @mock.patch("time.time")
    def test_values_method_simple_1(self, mocked_time):
        mocked_time.return_value = 10000.0
        fields = ["sell_currency", "sell_amount", "buy_currency", "buy_amount", "rate"]
        values = ["GBP", 100.0, "USD", 140.0, 1.4]
        self.assertEqual(Trade(**dict(zip(fields, values))).values(), values + [10000.0])

    def test_values_method_fails_validation_1(self):
        fields = ["sell_currency", "sell_amount", "buy_currency", "buy_amount", "rate"]
        values = ["GBP", -100.0, "USD", -140.0, 1.4]
        self.assertRaises(ValueError, Trade, **dict(zip(fields, values)))


if __name__ == "__main__":
    unittest.main()