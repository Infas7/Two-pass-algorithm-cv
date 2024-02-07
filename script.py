import cv2
import numpy as np
import random

label_array = []
label_conv = {}


def find_label(pixels):
    if all(x == 0 for x in pixels):
        if len(label_array) == 0:
            label_array.append(1)
            return max(label_array)
        else:
            label_array.append(max(label_array) + 1)
            return max(label_array)

    else:
        pixels = [x for x in pixels if x != 0]
        pixels.sort()

        minimum = pixels[0]
        maximum = pixels[len(pixels) - 1]

        if maximum == minimum:
            return minimum
        else:
            label_conv[maximum] = minimum
            return minimum


# Two pass algorithm
def find_connected_components(image):
    row, col = image.shape

    # First Pass
    for i in range(row):
        for j in range(col):
            if image[i, j] == 1:
                if i == 0 and j == 0:
                    image[i, j] = find_label([])
                elif i == 0 and j > 0:
                    image[i, j] = find_label([image[i, j - 1]])
                else:
                    image[i, j] = find_label([image[i - 1, j], image[i, j - 1]])

    # Second Pass
    for index in range(len(label_conv)):
        for i in range(row):
            for j in range(col):
                if image[i][j] in label_conv:
                    image[i][j] = label_conv[image[i][j]]

    return image


def convert_to_color(image):
    row, col = image.shape

    label_color = {0: (0, 0, 0)}
    colored_image = np.zeros((row, col, 3), int)

    for i in range(row):
        for j in range(col):
            label = image[i, j]
            if label not in label_color:
                label_color[label] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            colored_image[i, j, :] = label_color[label]

    return colored_image




image = cv2.imread("Sample Image 1.png", cv2.IMREAD_GRAYSCALE)
image = cv2.copyMakeBorder(image,1,1,1,1,cv2.BORDER_CONSTANT, value=0)

for i in range(len(image)):
    for j in range(len(image[0])):
        image[i][j] = 1 if image[i][j] > 100 else 0

passed_img = find_connected_components(image)
coloured_img = convert_to_color(passed_img)

cv2.imwrite("output-image.jpg", coloured_img)
print('Completed....')


