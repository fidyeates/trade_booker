import tornado.ioloop
import tornado.web
from data_layer.schema import Trade
from data_layer.rates import get_all_symbols, get_rate
import json
import sqlite3
import os

WEBSERVER_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class ListingsHandler(tornado.web.RequestHandler):
    """
    The tornado web handler for handling requests to list all Trades,

    Supported methods: get
    """
    def get(self):
        try:
            trades = list(Trade.fetch_all())
        except sqlite3.OperationalError:
            # The table has not been created yet
            print("Error, you first need to have run setup.sh or bin/setup.sh")
            trades = []
        self.render("templates/list_view.html", title="Trade Booker - List", trades=trades)


class BookingHandler(tornado.web.RequestHandler):
    """
    The tornado web handler for handling requests to create new Trades

    Supported methods: get, post
    """
    SYMBOLS = get_all_symbols()

    def get(self):
        self.render("templates/booking.html", title="Trade Booker - Booking", symbols=self.SYMBOLS)

    def post(self):
        raw_data = self.request.body
        data = json.loads(raw_data)
        data["sell_amount"] = float(data["sell_amount"])
        data["buy_amount"] = float(data["buy_amount"])
        data["rate"] = float(data["rate"])
        Trade(**data).save()
        self.write({"success": True})


class RateHandler(tornado.web.RequestHandler):

    def post(self):
        raw_data = self.request.body
        try:
            data = json.loads(raw_data)
            rate = get_rate(data["from"], data["to"])
            payload = {
                "success": True,
                "rate": rate
            }
        except:
            payload = {"success": False}
        self.write(payload)


def make_app():
    """
    Helper function to create a tornado application.
    :rtype: tornado.web.Application
    """
    return tornado.web.Application([
        (r"/", ListingsHandler),
        (r"/book", BookingHandler),
        (r"/rates", RateHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": WEBSERVER_DIRECTORY + "/static/"},),
    ])


def run():
    """
    Runner function to handle the setup and blocking call to start a tornado webserver, shutdown on sigint
    """
    app = make_app()
    app.listen(8888)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Exiting")


if __name__ == "__main__":
    run()