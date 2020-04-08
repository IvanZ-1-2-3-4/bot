import numpy as np
import time
import wget
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from skimage import io
from skimage import color
from skimage import transform
from skimage.viewer import ImageViewer as image_viewer # oh image viewer you little bitchfucker listen here you think you're so damn cool and clever and edgy going against conventions and naming your fucking variables with camelcase when you know FULL WELL that the convention is to use underscore well let me tell you what, you just got fucking outsmarted in the most humiliating and simply elegant manner possible. so maybe reconsider your fucking decision of being a special little snowflake hm? make the code a little more readable and gain a smidge of fucking respect from actual coders, or yknow, don't, not that I care since I can just rename your bullshit however i like since that's how python works, not that you'd know anything about that
from net import M, n
import wget

image_counter = 0
wget.download("https://cdn.vox-cdn.com/thumbor/T4J2eqER_Boh32R6p1Ennwkj8sM=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/3904558/boromirmeme.jpg", "images/temp.png")

# resize image to have an area of target_image_size, but maintain aspect ratio
print(os.path.abspath("images/temp.png"))
edit_image = io.imread(os.path.abspath("images/temp.png"))
# convert to grayscale
edit_image = color.rgb2gray(edit_image)
target_image_size = 200*263
h = len(edit_image)
w = len(edit_image[0])
aspect_ratio = w / h
hp = int(np.sqrt(target_image_size / aspect_ratio))
wp = int(np.sqrt(target_image_size * aspect_ratio))
edit_image = transform.resize(edit_image, (hp, wp))
# split image into MxM grids and save grids
current_position = {"row": 0, "col": 0}
# duplicates of pixels in more than one image are only allowed if that image has at max half duplicate pixels
while (hp - current_position["row"]) > 0:
    # if space left
    while (wp - current_position["col"]) > 0:
        grid = None
        # if current position is between M / 2 and M, so duplicate
        if (wp - current_position["col"]) < M:
            if (wp - current_position["col"]) > (M / 2):
                current_position["col"] = wp - M
                grid = edit_image[current_position["row"] : current_position["row"] + M, current_position["col"] : current_position["col"] + M]
                current_position["col"] = current_position["col"] + M + 1 # will stop the loops
            else:
                current_position["col"] = current_position["col"] + M
        else:
            grid = edit_image[current_position["row"] : current_position["row"] + M, current_position["col"] : current_position["col"] + M]
            current_position["col"] = current_position["col"] + M

        if grid is not None:
            io.imsave("images/training_set/{0}.png".format(image_counter), grid)
            image_counter = image_counter + 1
    
    current_position["col"] = 0

    if (hp - (current_position["row"] + M)) < M:
        if (hp - (current_position["row"] + M)) > (M / 2):
            current_position["row"] = hp - M
        else:
            current_position["row"] = current_position["row"] + 2*M # will stop the loop
    else:
        current_position["row"] = current_position["row"] + M
