from datetime import datetime

import plotly.graph_objects as go

from sqlitedict import SqliteDict
import matplotlib.pyplot as plt

class Indicator:
    def __init__(self, symbol, ticker, timeframe, date_time, name):
        self.cache = SqliteDict(f"data/indicator_{name}_{timeframe}_{symbol}.db")
        self.symbol = symbol
        self.ticker = ticker
        self.timeframe = timeframe
        self.date_time = date_time or datetime.now()

    def get_bar(self, bar_number: int):
        pass

    @staticmethod
    def date_to_string(date):
        return date.strftime("%d %b %Y %H:%M:%S")

    def draw(self, to_bar=10, from_bar=0):
        datapoints = [self.get_bar(i) for i in range(to_bar, from_bar, -1)]
        # plt.plot(datapoints)
        # plt.ylabel('Price')
        # plt.xlabel(f'Bars - {self.timeframe}')
        # plt.show()

        data_dictionary = {
            'timestamp': [p['timestamp'] for p in datapoints],
            'open': [p['open'] for p in datapoints],
            'high': [p['high'] for p in datapoints],
            'low': [p['low'] for p in datapoints],
            'close': [p['close'] for p in datapoints],
            'volume': [p['volume'] for p in datapoints],
        }

        fig = go.Figure(data=[go.Candlestick(x=data_dictionary['timestamp'],
                                             open=data_dictionary['open'],
                                             high=data_dictionary['high'],
                                             low=data_dictionary['low'],
                                             close=data_dictionary['close'])])
        fig.show()