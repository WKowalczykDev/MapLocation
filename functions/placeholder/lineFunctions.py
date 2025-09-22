from shapely.geometry import Point


def line_equation(p1: Point, p2: Point):
    # współczynniki kierunkowe (nachylenie)
    if p1.x == p2.x:
        # pionowa linia
        return None, p1.x

    m = (p2.y - p1.y) / (p2.x - p1.x)  # nachylenie (slope)
    b = p1.y - m * p1.x  # wyraz wolny
    return m, b


def y_from_x(p1: Point, p2: Point, x: float) -> float:
    m, b = line_equation(p1, p2)
    if m is None:
        raise ValueError("Linia pionowa – nie da się obliczyć y dla x")
    return m * x + b


def x_from_y(p1: Point, p2: Point, y: float) -> float:
    m, b = line_equation(p1, p2)
    if m is None:
        return p1.x
    return (y - b) / m


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
