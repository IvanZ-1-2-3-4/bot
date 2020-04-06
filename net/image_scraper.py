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

getRequest = "https://www.google.com/search?q=impact+font+memes&tbm=isch&ved=2ahUKEwi55b-4xczoAhVCTqwKHX61DOIQ2-cCegQIABAA&oq=impact+font+memes&gs_lcp=CgNpbWcQAzICCAAyAggAMgIIADIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIECAAQGDoECAAQQ1CWAljTFGC8FWgCcAB4AIABZ4gB5gmSAQQxOC4xmAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img&ei=RFKHXrmzJ8KcsQX-6rKQDg&bih=937&biw=1920"
timeDelay = 1
shortTimeDelay = 0.1

wd = webdriver.Chrome(executable_path = r"C:\\Users\\Ivab\\Desktop\\Programs n stuffies\\bot\\net\\chromedriver.exe")
wd.get(getRequest)

# is the right way of doing things
def findByXpath(xpath):
    try:
        out = wd.find_element_by_xpath(xpath)
        return out
    except:
        return False

# scroll to bottom
while not findByXpath("//div[@class=\"OuJzKb Bqq24e\" and text()=\"Looks like you've reached the end\"]"):
    # load more button
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    if findByXpath("//div[@class=\"YstHxe\"]").is_displayed():
        button = wd.find_element_by_xpath("//input[@class=\"mye4qd\"]")
        button.click()
wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")


imageCounter = 0
for img in wd.find_elements_by_css_selector("img.rg_i"):
    try:
        img.click()
        time.sleep(timeDelay)
        for actualImage in wd.find_elements_by_xpath("//img[@class=\"n3VNCb\"]"):
            if actualImage.is_displayed():
                imageCounter = processImage(actualImage, imageCounter)
        time.sleep(shortTimeDelay)
    except Exception:
        continue

def processImage(image, imageCounter):
    # download image
    src = image.get_attribute("src")
    wget.download(src, "images/temp.png")

    # resize image to have an area of targetImageSize, but maintain aspect ratio
    editImage = io.imread(os.path.abspath("images/temp.png"))
    # convert to grayscale
    editImage = color.rgb2gray(editImage)
    h = len(editImage)
    w = len(editImage[0])
    aspectRatio = w / h
    hNew = int(np.sqrt(targetImageSize / aspectRatio))
    wNew = int(hNew, np.sqrt(targetImageSize * aspectRatio))
    transform.resize(editImage, (hNew, wNew))

    # split image into MxM grids and save grids
    currentPosition = {"col": 0, "row": 0}
    # duplicates of pixels in more than one image are only allowed if that image has at max half duplicate pixels
    while (hNew - currentPosition["row"]) > 0:
        rowIncrement = M
        # if space left
        while (wNew - currentPosition["col"]) > 0:
            grid = None
            # if current position is between M / 2 and M, so duplicate
            if (wNew - currentPosition["col"]) < M:
                if (wNew - currentPosition["col"]) > (M / 2):
                    grid = editImage[currentPosition["row"] : currentPosition["row"] + rowIncrement][-1: -M]
                    currentPosition["col"] = 0
                else:
                    currentPosition["col"] = 0
            else:
                grid = editImage[currentPosition["row"] : currentPosition["row"] + rowIncrement][currentPosition["col"] : currentPosition["col"] + M]
                currentPosition["col"] = currentPosition["col"] + M

            imageCounter = imageCounter + 1    
            io.imsave("images/training_set/{0}.png", grid)
            
        if (hNew - (currentPosition["row"] + M)) < M:
            if (hNew - (currentPosition["row"] + M)) > M / 2:
                currentPosition["row"] = -1
                rowIncrement = -M
        else:
            currentPosition["row"] = currentPosition["row"] + M
    
    # return imageCounter to keep track of counter SINCE YOU CAN'T PASS BY REFERENCE
    return imageCounter
    
    os.remove("images/temp.png")