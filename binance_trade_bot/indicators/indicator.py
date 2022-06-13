from datetime import datetime

import plotly.graph_objects as go

from sqlitedict import SqliteDict

from binance_trade_bot.utils import trim_date_to_timeframe, timeframe_to_timedelta, date_to_string


class Indicator:
    def __init__(self, symbol, ticker, timeframe, date_time, name, config, logger):
        self.cache = SqliteDict(f"data/indicator_{name}_{timeframe}_{symbol}.db")
        self.symbol = symbol
        self.ticker = ticker
        self.config = config
        self.logger = logger
        self.timeframe = timeframe
        self.date_time = trim_date_to_timeframe(
            date_time or datetime.now(), self.timeframe
        )
        self.figure = None

    def has_history(self, count=10):
        for i in range(count):
            if not self.is_bar_in_cache(i):
                return False
        return True

    def get_bar_date(self, bar):
        return self.date_time - bar * timeframe_to_timedelta(self.timeframe)

    def get_bar_cache_key(self, bar):
        date = self.get_bar_date(bar)
        date_string = date_to_string(date)
        return f"{self.symbol} - {date_string}"

    def is_bar_in_cache(self, bar):
        return self.get_bar_cache_key(bar) in self.cache

    def get_bar(self, bar_number: int):
        key = self.get_bar_cache_key(bar_number)
        if key in self.cache:
            return self.cache.get(key)

        value = self.bar(bar_number)
        self.cache[key] = value
        self.cache.commit()
        return value

    def draw(self):
        if not self.figure:
            self.figure = go.Figure()

    def bar(self, bar_number):
        raise NotImplemented("You need to implement bar method")
