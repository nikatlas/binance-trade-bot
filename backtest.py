import sys
from datetime import datetime

from sqlitedict import SqliteDict

from binance_trade_bot import backtest

EXTREME_BEAR = (datetime(2022, 5, 1), datetime(2022, 5, 2)) #16
EXTREME_BULL = (datetime(2020, 12, 10), datetime(2020, 12, 11)) #28


def run_test(date_range, mode):
    cache = SqliteDict(f"data/backtest_cache_{mode}.db")
    history = []
    start_date, end_date = date_range
    last_manager = None
    for manager in backtest(start_date, end_date, yield_interval=10000, cache=cache):
        btc_value = manager.collate_coins("BTC")
        bridge_value = manager.collate_coins(manager.config.BRIDGE.symbol)
        history.append((btc_value, bridge_value))
        btc_diff = round((btc_value - history[0][0]) / history[0][0] * 100, 3)
        bridge_diff = round((bridge_value - history[0][1]) / history[0][1] * 100, 3)
        print("------")
        print("TIME:", manager.datetime)
        print("BALANCES:", manager.balances)
        print("BTC VALUE:", btc_value, f"({btc_diff}%)")
        print(f"{manager.config.BRIDGE.symbol} VALUE:", bridge_value, f"({bridge_diff}%)")
        print("------")
        last_manager = manager
    return last_manager


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Call with xbull or xbear argument")
        exit(0)

    mode = sys.argv[1]
    if mode == 'xbear':
        manager = run_test(EXTREME_BEAR, mode)
    elif mode == 'xbull':
        manager = run_test(EXTREME_BULL, mode)

    print(f"Mode[{mode}] manager value: {manager.collate_coins(manager.config.BRIDGE.symbol)}")

