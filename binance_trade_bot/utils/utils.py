from datetime import timedelta, datetime


def ohlcv_to_dictionary(ohlcv):
    timestamp, open_price, high, low, close, volume, *rest = ohlcv
    return {
        "timestamp": timestamp,
        "open": float(open_price),
        "high": float(high),
        "low": float(low),
        "close": float(close),
        "volume": float(volume),
    }


def group_by_key(array):
    return {
        "timestamp": [
            date_to_string(datetime.fromtimestamp(p["timestamp"] / 1000))
            for p in array
            if p
        ],
        "open": [p["open"] for p in array if p],
        "high": [p["high"] for p in array if p],
        "low": [p["low"] for p in array if p],
        "close": [p["close"] for p in array if p],
        "volume": [p["volume"] for p in array if p],
    }


def timeframe_to_timedelta(timeframe):
    minutes = 0
    if "m" in timeframe:
        minutes = int(timeframe.replace("m", ""))
    if "h" in timeframe:
        minutes = int(timeframe.replace("h", "")) * 60
    if "d" in timeframe:
        minutes = int(timeframe.replace("d", "")) * 60 * 24
    if "w" in timeframe:
        minutes = int(timeframe.replace("w", "")) * 60 * 24 * 7
    return timedelta(minutes=minutes)


def trim_date_to_timeframe(dt, timeframe):
    time_dt = timeframe_to_timedelta(timeframe)

    return dt + (datetime.min - dt) % time_dt


def date_to_string(date):
    return date.strftime("%d %b %Y %H:%M:%S")
