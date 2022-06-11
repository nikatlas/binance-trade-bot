from datetime import datetime

from binance_trade_bot.utils import trim_date_to_timeframe


def test_trim_date():
    return trim_date_to_timeframe(datetime.now(), "5m")


print(test_trim_date())
