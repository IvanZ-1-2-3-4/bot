import numpy as np
import time
import wget
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from skimage import io
from skimage import color
from skimage import transform
from skimage.viewer import ImageViewer as image_viewer # oh image viewer you little bitchfucker listen here you think you're so damn cool and clever and edgy going against conventions and naming your fucking letiables with camelcase when you know FULL WELL that the convention is to use underscore well let me tell you what, you just got fucking outsmarted in the most humiliating and simply elegant manner possible. so maybe reconsider your fucking decision of being a special little snowflake hm? make the code a little more readable and gain a smidge of fucking respect from actual coders, or yknow, don't, not that I care since I can just rename your bullshit however i like since that's how python works, not that you'd know anything about that
from net3 import M, n
from urllib.error import HTTPError, URLError
import pickle
import sys

if not (len(sys.argv) == 2):
    raise SystemExit('ERROR: pass google url to be scraped as single argument')

get_request = sys.argv[1]

# words = sys.argv[1].split('&q')[1].split('&oq')[0].split('=')[1].split('+')
# print_string = 'Scraping google images for search query "' + words[0]
# for word in words[1::]:
#     print_string = print_string + ' ' + word
# print(print_string + '"')

target_image_size = M**2 * n
time_delay = 1
short_time_delay = 0.1

# net_images_folder_id = '1K3gh-dgHkkIgV1XrNTIegzwmPc96VU0A'
# creds = pickle.load(open('token.pickle', 'rb'))
# service = build('drive', 'v3', credentials=creds)

wd = webdriver.Chrome(executable_path = r'C:\\bin\\chromedriver.exe') # put driver in c:\bin
wd.get(get_request)

# this is the right way of doing things
def find_by_xpath(xpath):
    try:
        out = wd.find_element_by_xpath(xpath)
        return out
    except:
        return False

# def upload_image(img_name, img_url):
#     try:
#         file_metadata = {'name': img_name, 'parents': [net_images_folder_id]}
#         media = MediaFileUpload(img_url, mimetype='image/png')
#         service.files().create(body = file_metadata, media_body = media, fields = 'id').execute()
#     except:
#         pass

def process_image(image, image_counter):
    try:
        # download image
        src = image.get_attribute('src')
        wget.download(src, 'images/temp.png')
        # resize image to have an area of target_image_size, but maintain aspect ratio
        edit_image = io.imread(os.path.abspath('images/temp.png'))
        # convert to grayscale
        edit_image = color.rgb2gray(edit_image)
        h = len(edit_image)
        w = len(edit_image[0])
        aspect_ratio = w / h
        hp = int(np.sqrt(target_image_size / aspect_ratio))
        wp = int(np.sqrt(target_image_size * aspect_ratio))
        edit_image = transform.resize(edit_image, (hp, wp))
        # split image into MxM grids and save grids
        
        # split image into MxM grids and save grids
        current_position = {'row': 0, 'col': 0}
        # duplicates of pixels in more than one image are only allowed if that image has at max half duplicate pixels
        while (hp - current_position['row']) > 0:
            # if space left
            while (wp - current_position['col']) > 0:
                grid = None
                # if current position is between M / 2 and M, so duplicate
                if (wp - current_position['col']) < M:
                    if (wp - current_position['col']) > (M / 2):
                        current_position['col'] = wp - M
                        grid = edit_image[current_position['row'] : current_position['row'] + M, current_position['col'] : current_position['col'] + M]
                        current_position['col'] = wp + 1 # will stop the loops
                    else:
                        current_position['col'] = current_position['col'] + M
                else:
                    grid = edit_image[current_position['row'] : current_position['row'] + M, current_position['col'] : current_position['col'] + M]
                    current_position['col'] = current_position['col'] + M

                if grid is not None:
                    img_name = '{0}.png'.format(image_counter)
                    img_url = 'images/{0}'.format(img_name)
                    io.imsave(img_url, grid)
                    # upload_image(img_name, img_url)
                    os.remove(img_url)
                    image_counter = image_counter + 1
            
            current_position['col'] = 0

            if (hp - (current_position['row'] + M)) < M:
                if (hp - (current_position['row'] + M)) > (M / 2):
                    current_position['row'] = hp - M
                else:
                    current_position['row'] = hp + 1 # will stop the loop
            else:
                current_position['row'] = current_position['row'] + M
    except (ValueError, HTTPError, URLError):
        pass

    try: os.remove('images/temp.png')
    except: pass
    # return image_counter to keep track of counter SINCE YOU CAN'T PASS BY REFERENCE
    return image_counter

def process_image_whole(image, image_counter):
    counter_local = image_counter
    try:
        # download image
        src = image.get_attribute('src')
        wget.download(src, 'images/temp.png')
        
        edit_image = io.imread(os.path.abspath('images/temp.png'))

        target_image_dimension = 100
        edit_image = transform.resize(edit_image, (target_image_dimension, target_image_dimension))
        
        # convert to grayscale
        edit_image = color.rgb2gray(edit_image)

        # save image
        io.imsave(f'images/net_images_whole/{image_counter}.png', edit_image)

        counter_local += 1
    except (HTTPError, URLError, ValueError):
        pass
    try: os.remove('images/temp.png')
    except: pass
    return counter_local

# scroll to bottom
while not find_by_xpath("//div[@class=\"OuJzKb Bqq24e\" and text()=\"Looks like you've reached the end\"]"):
    # load more button
    wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    if find_by_xpath('//div[@class=\'YstHxe\']').is_displayed():
        button = wd.find_element_by_xpath('//input[@class=\'mye4qd\']')
        button.click()
wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')

image_counter = 505
for img in wd.find_elements_by_css_selector('img.rg_i'):
    try:
        img.click()
        time.sleep(time_delay)
    except Exception:
        continue
    for actual_image in wd.find_elements_by_xpath('//img[@class=\'n3VNCb\']'):
        if actual_image.is_displayed():
            image_counter = process_image_whole(actual_image, image_counter)
    time.sleep(short_time_delay)