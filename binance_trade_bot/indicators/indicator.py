from datetime import datetime

import plotly.graph_objects as go

from sqlitedict import SqliteDict
import matplotlib.pyplot as plt


class Indicator:
    def __init__(self, symbol, ticker, timeframe, date_time, name, config, logger):
        self.cache = SqliteDict(f"data/indicator_{name}_{timeframe}_{symbol}.db")
        self.symbol = symbol
        self.ticker = ticker
        self.config = config
        self.logger = logger
        self.timeframe = timeframe
        self.date_time = date_time or datetime.now()
        self.figure = None

    def get_bar(self, bar_number: int):
        pass

    @staticmethod
    def date_to_string(date):
        return date.strftime("%d %b %Y %H:%M:%S")

    def draw(self):
        if not self.figure:
            self.figure = go.Figure()
