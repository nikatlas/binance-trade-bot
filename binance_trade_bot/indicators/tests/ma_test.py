from datetime import datetime

from binance_trade_bot.indicators import MA
from binance_trade_bot.indicators.price import Price
from binance_trade_bot.config import Config
from binance_trade_bot.logger import Logger

config = Config()
price_indicator = Price(symbol="COTIUSDT",
                        timeframe="5m",
                        logger=Logger(), config=config,
                        date_time=datetime.strptime('Jun 4 2022  06:00PM', '%b %d %Y %I:%M%p'))

price_indicator.get_history()

ma_indicator = MA.from_price(price_indicator, depth=10)

ma_indicator.draw(to_bar=100, silent=True)

ma_indicator_20 = MA.from_price(price_indicator, depth=20)
ma_indicator_20.draw(to_bar=100)