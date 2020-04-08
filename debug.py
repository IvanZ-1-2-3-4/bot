import numpy as np
import time
import wget
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from skimage import io
from skimage import color
from skimage import transform
from skimage import viewer
from net import M, n
import wget
import math

image_counter = 0
#wget.download("https://pics.me.me/meme-text-impact-font-with-outline-ww-ss-best-font-for-51930413.png", "images/temp.png")

# resize image to have an area of targetImageSize, but maintain aspect ratio
print(os.path.abspath("images/temp.png"))
edit_image = io.imread(os.path.abspath("images/temp.png"))
# convert to grayscale
edit_image = color.rgb2gray(edit_image)
targetImageSize = 200*263
h = len(edit_image)
w = len(edit_image[0])
aspectRatio = w / h
h_prime = int(np.sqrt(targetImageSize / aspectRatio))
w_prime = int(np.sqrt(targetImageSize * aspectRatio))
edit_image = transform.resize(edit_image, (h_prime, w_prime))
io.imsave("images/final.png", edit_image)
# split image into MxM grids and save grids
current_position = {"col": 0, "row": 0}
# duplicates of pixels in more than one image are only allowed if that image has at max half duplicate pixels
while (h_prime - current_position["row"]) > 0:
    row_increment = M
    # if space left
    while (w_prime - current_position["col"]) > 0:
        grid = None
        # if current position is between M / 2 and M, so duplicate
        if (w_prime - current_position["col"]) < M:
            if (w_prime - current_position["col"]) > (M / 2):
                grid = edit_image[current_position["row"] : current_position["row"] + row_increment][-1: -M]
                current_position["col"] = 0
            else:
                current_position["col"] = 0
        else:
            grid = edit_image[current_position["row"] : current_position["row"] + row_increment][current_position["col"] : current_position["col"] + M]
            current_position["col"] = current_position["col"] + M

        io.imsave("images/training_set/{0}.png".format(image_counter), grid)
        image_counter = image_counter + 1
        
    if (h_prime - (current_position["row"] + M)) < M:
        if (h_prime - (current_position["row"] + M)) > (M / 2):
            current_position["row"] = -1
            row_increment = -M
    else:
        current_position["row"] = current_position["row"] + M
