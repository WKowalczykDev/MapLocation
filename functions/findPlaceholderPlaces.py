from constants import w_placeholder, h_placeholder
from functions.placeholder.distance import distance
from functions.placeholder.lineFunctions import sign, y_from_x, x_from_y
from shapely.geometry import Point

def findPlaceholderPlaces(centerPoints):
    print("Center point: ", centerPoints)

    fixedPoints = []

    for cp in centerPoints:
        print("Center point: ", cp)
        collision = False
        for fp in fixedPoints[:]:
            d = distance(cp, fp)
            if abs(d.x) < w_placeholder and abs(d.y) < h_placeholder:
                print('Mamy zbyt bliskie sąsiedztwo: ', cp, fp)
                collision = True
                # przypadek na szerokość
                if abs(d.x) > abs(d.y):
                    print("szerokosc")
                    final_px = cp.x+(w_placeholder-abs(d.x))*sign(d.x)
                    final_py = y_from_x(cp,fp,final_px)
                    fixedPoints.append(Point(final_px, final_py))
                # przypadek na wysokosc
                else:
                    print("wysokosc")
                    final_py = cp.y + (h_placeholder - abs(d.y)) * sign(d.y)
                    fixedPoints.append(Point(x_from_y(cp, fp, final_py), final_py))

            #     tutaj bedzie funkcja która będzie sobie iść po linii i jak znajdzie to zajebiscie
            #   uciekamy po linii maksymalnie o połowe szerokości, bądź wysokości placeholdera, biorąc pod uwagę funkcję liniową pomiędzy tymi dwoma punktami

            else:
                print("jest git - nie zawadza")

        if not collision:
            fixedPoints.append(cp)


    print(fixedPoints)
    return fixedPoints



# import json
# with open("./../helpers/centerpoints_long.json", "r", encoding="utf-8") as f:
#     miasta = json.load(f)
#
#
# miasta = [Point(m["x"], m["y"]) for m in miasta]
# print(findPlaceholderPlaces(miasta))