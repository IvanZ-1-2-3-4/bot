import numpy as np
import time
import wget
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from skimage import io
from skimage import color
from net import M, n

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

# download every image
imageCounter = 0
for img in wd.find_elements_by_css_selector("img.rg_i"):
    try:
        img.click()
        time.sleep(timeDelay)
        for actualImage in wd.find_elements_by_xpath("//img[@class=\"n3VNCb\"]"):
            if actualImage.is_displayed():
                # download image
                src = actualImage.get_attribute("src")

                fileType = ""
                if len(src) > 1500:
                    if "jpeg" in src:
                        fileType = "jpg"
                    elif "png" in src:
                        fileType = "png"
                else:
                    fileType = src[-1:-3]

                wget.download(src, "images/temp.{0}".format(fileType))

                # split image into MxM grids
                editImage = io.imread(os.path.abspath("images/temp.{0}".format(fileType)))
                editImage = color.rgb2gray(editImage)
                
                imageCounter = imageCounter + 1
        time.sleep(shortTimeDelay)
    except Exception:
        continue