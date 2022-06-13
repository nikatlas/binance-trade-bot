from datetime import datetime

from binance_trade_bot.indicators import MA
from binance_trade_bot.indicators.price import Price
from binance_trade_bot.config import Config
from binance_trade_bot.indicators.vp import VP
from binance_trade_bot.logger import Logger

config = Config()
price_indicator = Price(
    symbol="COTIUSDT",
    timeframe="5m",
    logger=Logger(),
    config=config,
    date_time=datetime.now(),
    #date_time=datetime.strptime('Dec 4 2021  06:00PM', '%b %d %Y %I:%M%p')
)

has_history = price_indicator.has_history(100)
if not has_history:
    print("Fetching history")
    price_indicator.get_history(300)
price_indicator.draw(to_bar=100)

vp_indicator = VP.from_price(price_indicator, depth=100, resolution=20)

vp_indicator.draw()

peak, price = vp_indicator.is_price_near_peak()
print(peak, price)
