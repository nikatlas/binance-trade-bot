from datetime import datetime

import plotly.graph_objects as go

from sqlitedict import SqliteDict
import matplotlib.pyplot as plt

from binance_trade_bot.utils import trim_date_to_timeframe


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

    def get_bar(self, bar_number: int):
        pass

    def draw(self):
        if not self.figure:
            self.figure = go.Figure()
