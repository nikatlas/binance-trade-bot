from datetime import datetime
from math import floor

from plotly.subplots import make_subplots
from sqlitedict import SqliteDict

from binance_trade_bot.indicators import Indicator
import plotly.graph_objects as go

from binance_trade_bot.utils import group_by_key


class VP(Indicator):
    def __init__(
            self,
            depth,
            resolution,
            symbol,
            config,
            logger,
            timeframe="1m",
            date_time=datetime.strptime("Jun 1 2022  01:00PM", "%b %d %Y %I:%M%p"),
            ticker=None,
            bar_color='blue',
            peak_color='red'
    ):
        super().__init__(
            symbol,
            ticker=ticker or self,
            timeframe=timeframe,
            date_time=date_time,
            name="VP",
            config=config,
            logger=logger,
        )
        self.depth = depth
        self.resolution = resolution
        self.bar_color = bar_color
        self.peak_color = peak_color

    @staticmethod
    def find_peaks(data, ranges, limit=3):
        peaks = [{
            'value': peak,
            'index': index,
            'range': ranges[index]
        }
            for index, peak in enumerate(data) if peak >= data[index - 1 if index > 0 else 0] and peak >= data[
                index + 1 if index + 1 < len(data) else len(data) - 1]
        ]

        sorted_peaks = sorted(peaks, key=lambda x: -x['value'])
        return sorted_peaks[:limit]

    def is_price_near_peak(self, price=None):
        current_price = price or self.ticker.get_bar(0)
        data, ranges = self.get_bar(0)
        peaks = self.find_peaks(data, ranges)
        step = (ranges[0] + ranges[1]) / 2 - ranges[0]
        for peak in peaks:
            if abs(ranges[peak['index']] - current_price['close']) < 3 * step:
                return peak, current_price

        return False, current_price

    def bar(self, bar_number: int):
        if bar_number in self.cache:
            return self.cache.get(bar_number)
        rough_bars = [
            self.ticker.get_bar(bar_number + diff) for diff in range(self.depth)
        ]
        bars = [b for b in rough_bars if b]

        if not bars or not bars[0] or len(bars) < self.depth:
            return None, None

        min_price = min(bars, key=lambda x: x['low'])['low']
        max_price = max(bars, key=lambda x: x['high'])['high']
        step = (max_price - min_price) / self.resolution

        def find_index(price):
            return floor((price - min_price) / step)

        buckets = [0 for _ in range(self.resolution)]
        affected_by_bar_count = [0 for _ in range(self.resolution)]
        for index in range(len(buckets)):
            for bar in bars:
                volume = bar['volume']
                if find_index(bar['low']) <= index <= find_index(bar['high']):
                    buckets[index] += volume
                    affected_by_bar_count[index] += 1

        normalized_buckets = [0 for _ in range(self.resolution)]
        for index in range(len(buckets)):
            if affected_by_bar_count[index] > 0:
                normalized_buckets[index] = buckets[index] + buckets[index] / affected_by_bar_count[index]

        ranges = [min_price + index * step + step / 2 for index in range(self.resolution)]

        self.cache[bar_number] = (normalized_buckets, ranges)
        return normalized_buckets, ranges

    def draw(self, bar_number=0, silent=False):
        data, ranges = self.get_bar(bar_number)
        peaks = self.find_peaks(data, ranges)

        colors = [self.bar_color for _ in data]
        for peak in peaks:
            colors[peak['index']] = self.peak_color

        if not self.ticker.figure:
            self.ticker.draw(to_bar=bar_number + self.depth, from_bar=bar_number, silent=True)

        self.figure = make_subplots(figure=self.ticker.figure, specs=[[{"secondary_y": True}]])

        self.figure.update_layout(xaxis2={'anchor': 'y', 'overlaying': 'x', 'side': 'top'})

        self.figure.add_trace(
            # px.histogram(data, y="price", category_orders=dict(price=ranges))
            go.Bar(
                y=ranges,
                x=data,
                orientation='h',
                opacity=0.2,
                marker=dict(color=colors)
            ),
            secondary_y=False,
        )
        self.figure.data[-1].update(xaxis='x2')

        if not silent:
            self.figure.show()

    @staticmethod
    def from_price(indicator, depth, resolution):
        return VP(
            depth,
            resolution,
            indicator.symbol,
            indicator.config,
            indicator.logger,
            indicator.timeframe,
            indicator.date_time,
            indicator.ticker,
        )
