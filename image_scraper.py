import numpy as np
import time
import wget
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from skimage import io
from skimage import color
from skimage import transform
from net import M, n

targetImageSize = 200*263

get_request = "https://www.google.com/search?q=impact+font+memes&tbm=isch&ved=2ahUKEwi55b-4xczoAhVCTqwKHX61DOIQ2-cCegQIABAA&oq=impact+font+memes&gs_lcp=CgNpbWcQAzICCAAyAggAMgIIADIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIECAAQGDoECAAQQ1CWAljTFGC8FWgCcAB4AIABZ4gB5gmSAQQxOC4xmAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img&ei=RFKHXrmzJ8KcsQX-6rKQDg&bih=937&biw=1920"
time_delay = 1
short_time_delay = 0.1

wd = webdriver.Chrome(executable_path = r"C:\\Users\\Ivab\\Desktop\\Programs n stuffies\\bot\\net\\chromedriver.exe")
wd.get(get_request)

# is the right way of doing things
def find_by_xpath(xpath):
    try:
        out = wd.find_element_by_xpath(xpath)
        return out
    except:
        return False
"""
# scroll to bottom
while not find_by_xpath("//div[@class=\"OuJzKb Bqq24e\" and text()=\"Looks like you've reached the end\"]"):
    # load more button
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    if find_by_xpath("//div[@class=\"YstHxe\"]").is_displayed():
        button = wd.find_element_by_xpath("//input[@class=\"mye4qd\"]")
        button.click()
wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
"""

image_counter = 0
for img in wd.find_elements_by_css_selector("img.rg_i"):
    try:
        img.click()
        time.sleep(time_delay)
        for actual_image in wd.find_elements_by_xpath("//img[@class=\"n3VNCb\"]"):
            if actual_image.is_displayed():
                image_counter = processImage(actual_image, image_counter)
        time.sleep(short_time_delay)
    except Exception:
        continue

def processImage(image, image_counter):
    # download image
    src = image.get_attribute("src")
    wget.download(src, "images/temp.png")

    # resize image to have an area of targetImageSize, but maintain aspect ratio
    edit_image = io.imread(os.path.abspath("images/temp.png"))
    # convert to grayscale
    edit_image = color.rgb2gray(edit_image)
    h = len(edit_image)
    w = len(edit_image[0])
    aspectRatio = w / h
    h_prime = int(np.sqrt(targetImageSize / aspectRatio))
    w_prime = int(h_prime, np.sqrt(targetImageSize * aspectRatio))
    edit_image = transform.resize(edit_image, (h_prime, w_prime))
    
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
    
    # return image_counter to keep track of counter SINCE YOU CAN'T PASS BY REFERENCE
    return image_counter
    
    os.remove("images/temp.png")