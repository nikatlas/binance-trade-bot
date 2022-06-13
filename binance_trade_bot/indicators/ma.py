from datetime import datetime

from sqlitedict import SqliteDict

from binance_trade_bot.indicators import Indicator
import plotly.graph_objects as go

from binance_trade_bot.utils import group_by_key


class MA(Indicator):
    def __init__(
        self,
        depth,
        symbol,
        config,
        logger,
        timeframe="1m",
        date_time=datetime.strptime("May 1 2022  01:00PM", "%b %d %Y %I:%M%p"),
        ticker=None,
    ):
        super().__init__(
            symbol,
            ticker=ticker or self,
            timeframe=timeframe,
            date_time=date_time,
            name="MA",
            config=config,
            logger=logger,
        )
        self.depth = depth

    def bar(self, bar_number: int):
        rough_bars = [
            self.ticker.get_bar(bar_number + diff) for diff in range(self.depth)
        ]
        bars = [b for b in rough_bars if b]

        if not bars or not bars[0] or len(bars) < self.depth:
            return None

        keys = list(bars[0].keys())
        keys.remove("timestamp")

        result = {key: (sum([bar[key] for bar in bars]) / len(bars)) for key in keys}
        return {**result, "timestamp": bars[0]["timestamp"]}

    def draw(self, to_bar=10, from_bar=0, silent=False):
        data = [self.get_bar(i) for i in range(to_bar, from_bar, -1)]
        data_dict = group_by_key(data)

        if not self.ticker.figure:
            self.ticker.draw(to_bar=to_bar, from_bar=from_bar, silent=True)
        self.figure = self.ticker.figure
        self.figure.add_trace(
            go.Scatter(
                x=data_dict["timestamp"],
                y=data_dict["open"],
                mode="lines+markers",
                name="lines+markers",
            )
        )

        if not silent:
            self.figure.show()

    @staticmethod
    def from_price(indicator, depth):
        return MA(
            depth,
            indicator.symbol,
            indicator.config,
            indicator.logger,
            indicator.timeframe,
            indicator.date_time,
            indicator.ticker,
        )
