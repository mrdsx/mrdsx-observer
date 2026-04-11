def truncate(value: float, digits: int) -> float:
    value_str = str(value)
    before, dot, after = value_str.partition(".")
    return float(before + dot + after[:digits])
