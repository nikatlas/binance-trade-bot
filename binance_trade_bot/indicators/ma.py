from sqlitedict import SqliteDict

from binance_trade_bot.indicators import Indicator


class MA(Indicator):
    def __init__(self, symbol, ticker):
        super().__init__(symbol, ticker, name="MA")

    def calculate(self):
        pass
