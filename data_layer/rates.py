"""
Functionality for calls to 3rd party website fixer.io
"""
import urllib.request
import urllib.parse
import json

API_URL = "http://data.fixer.io/api"
ACCESS_KEY = "edfed567398eaeabd20a295428334ae3"


def get_all_symbols():
    """
    Get all available symbols form fixer.io as a list of string symbols

    :rtype: list[str]
    """
    uri = f"{API_URL}/symbols?access_key={ACCESS_KEY}"
    f = urllib.request.urlopen(uri)
    raw_data = f.read().decode('utf-8')
    return list(json.loads(raw_data)["symbols"].keys())


def get_rate(src_currency, to_currency):
    """
    Gets the current conversion rate from fixer.io

    :param str src_currency: The currency to convert from
    :param str to_currency: The currency to convert to
    :rtype: float
    """
    uri = f"{API_URL}/latest?access_key={ACCESS_KEY}&base={src_currency}&symbols={to_currency}"
    f = urllib.request.urlopen(uri)
    raw_data = f.read().decode('utf-8')
    return json.loads(raw_data)["rates"][to_currency]
