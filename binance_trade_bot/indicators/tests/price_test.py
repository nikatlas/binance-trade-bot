from datetime import datetime

from binance_trade_bot.indicators.price import Price
from binance_trade_bot.config import Config
from binance_trade_bot.logger import Logger

config = Config()
price_indicator = Price(symbol="COTIUSDT",
                        timeframe="5m",
                        logger=Logger(), config=config,
                        date_time=datetime.strptime('Jun 4 2022  06:00PM', '%b %d %Y %I:%M%p'))

price_indicator.get_history()

price_indicator.draw(to_bar=100)
