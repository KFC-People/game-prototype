import math


def map_exponential(
    value: float,
    in_min: float,
    in_max: float,
    out_min: float,
    out_max: float,
    alpha: float = 1,
) -> float:
    x_normal = (value - in_min) / (in_max - in_min)
    y_normal = math.exp(x_normal * alpha)

    return y_normal * (out_max - out_min) + out_min
