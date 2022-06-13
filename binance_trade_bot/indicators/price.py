from datetime import timedelta, datetime

from binance.client import Client

from binance_trade_bot.indicators import Indicator
from binance_trade_bot.utils import (
    ohlcv_to_dictionary,
    timeframe_to_timedelta,
    date_to_string,
)
import plotly.graph_objects as go

from binance_trade_bot.utils import group_by_key


class Price(Indicator):
    def __init__(
            self,
            symbol,
            config,
            logger,
            timeframe="1m",
            date_time=datetime.strptime("May 1 2022  01:00PM", "%b %d %Y %I:%M%p"),
    ):
        super().__init__(
            symbol,
            ticker=self,
            timeframe=timeframe,
            date_time=date_time,
            name="price",
            config=config,
            logger=logger,
        )

        self.binance_client = Client(
            config.BINANCE_API_KEY,
            config.BINANCE_API_SECRET_KEY,
            tld=config.BINANCE_TLD,
        )

    def get_history(self, count):
        start_date = self.date_time - (count+10) * timeframe_to_timedelta(self.timeframe)
        start_date = date_to_string(start_date)
        end_date = self.date_time
        end_date = date_to_string(end_date)
        if self.logger is not None:
            self.logger.info(
                f"[Price Indicator]Fetching prices for {self.symbol} between {end_date} and {self.date_time}"
            )
        for result in self.binance_client.get_historical_klines(
            self.symbol, self.timeframe, start_date, end_date, limit=1000
        ):
            date = date_to_string(datetime.fromtimestamp(result[0] / 1000))
            self.cache[f"{self.symbol} - {date}"] = ohlcv_to_dictionary(result)
        self.cache.commit()

    def bar(self, bar):
        raise KeyError("Value has not been fetched!", self.get_bar_cache_key(bar))

    def draw(self, to_bar=10, from_bar=0, silent=False):
        super().draw()

        datapoints = [self.get_bar(i) for i in range(to_bar, from_bar, -1)]
        data_dictionary = group_by_key(datapoints)

        self.figure.add_trace(
            go.Candlestick(
                x=data_dictionary["timestamp"],
                open=data_dictionary["open"],
                high=data_dictionary["high"],
                low=data_dictionary["low"],
                close=data_dictionary["close"],
            )
        )
        if not silent:
            self.figure.show()
