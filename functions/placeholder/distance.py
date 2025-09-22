from shapely.geometry import Point

def distance(point1, point2):
    return Point(point1.x - point2.x, point1.y - point2.y)