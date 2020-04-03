import requests
from bs4 import BeautifulSoup
import wget
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
wd = webdriver.Chrome(executable_path="chromedriver.exe")
wd.get('https://google.com')
request = requests.get("https://www.google.com/search?q=impact+font+memes&tbm=isch&ved=2ahUKEwi55b-4xczoAhVCTqwKHX61DOIQ2-cCegQIABAA&oq=impact+font+memes&gs_lcp=CgNpbWcQAzICCAAyAggAMgIIADIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIECAAQGDoECAAQQ1CWAljTFGC8FWgCcAB4AIABZ4gB5gmSAQQxOC4xmAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img&ei=RFKHXrmzJ8KcsQX-6rKQDg&bih=937&biw=1920")

soup = BeautifulSoup(request.content, "html.parser")

counter = 0
for link in soup.find_all("img"):
    if (link.get("src") == None) or ("google" in link.get("src")):
        pass
    else:
        image = wget.download(link.get("src"), "images/{0}.png".format(counter))
        counter = counter + 1
