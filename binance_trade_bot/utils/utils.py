
def ohlcv_to_dictionary(ohlcv):
    timestamp, open_price, high, low, close, volume, *rest = ohlcv
    return {
        'timestamp': timestamp,
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    }