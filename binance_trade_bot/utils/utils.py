def ohlcv_to_dictionary(ohlcv):
    timestamp, open_price, high, low, close, volume, *rest = ohlcv
    return {
        'timestamp': timestamp,
        'open': float(open_price),
        'high': float(high),
        'low': float(low),
        'close': float(close),
        'volume': float(volume)
    }


def group_by_key(array):
    return {
        'timestamp': [p['timestamp'] for p in array],
        'open': [p['open'] for p in array],
        'high': [p['high'] for p in array],
        'low': [p['low'] for p in array],
        'close': [p['close'] for p in array],
        'volume': [p['volume'] for p in array],
    }
