import cv2
import numpy as np

# Wczytaj obraz
img = cv2.imread('mapa_A2.png')

# Konwertuj na HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Zakres czerwonego
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# Maska dla czerwonego
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)

# Znajdź kontury czerwonej ramki
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour = max(contours, key=cv2.contourArea)

# Stwórz maskę tylko dla wnętrza konturu
mask_inside = np.zeros_like(mask)
cv2.drawContours(mask_inside, [contour], -1, 255, thickness=-1)  # wypełniony kontur
mask_inside = cv2.bitwise_and(mask_inside, cv2.bitwise_not(mask))  # usuń sam czerwony obrys

# Wytnij obszar prostokątny wokół konturu
x, y, w, h = cv2.boundingRect(contour)
roi = cv2.bitwise_and(img[y:y+h, x:x+w], img[y:y+h, x:x+w], mask=mask_inside[y:y+h, x:x+w])

# Zapisz wynik
cv2.imwrite('wyciety_obraz.png', roi)
