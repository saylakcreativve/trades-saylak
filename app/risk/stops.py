def atr_stop(entry: float, atr: float, multiplier: float = 2.0, direction: str = "LONG") -> float:
    if atr <= 0:
        raise ValueError("ATR must be positive")
    return entry - atr * multiplier if direction.upper() == "LONG" else entry + atr * multiplier


def rr_target(entry: float, stop: float, rr: float = 2.0, direction: str = "LONG") -> float:
    risk = abs(entry - stop)
    return entry + risk * rr if direction.upper() == "LONG" else entry - risk * rr
