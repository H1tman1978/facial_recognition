#! /usr/bin/python
import shutil
import requests
import sys
from bs4 import BeautifulSoup as soup


def get_source(link):
    r = requests.get(link)
    if r.status_code == 200:
        return soup(r.text)
    else:
        sys.exit("[~] Invalid Response Received.")


def filter_images(html):
    imgs = html.findAll("img", attrs={'class': lambda x: x and 'user-photo' and 'preload' and 'loaded' in x.split()})
    if imgs:
        return imgs
    else:
        sys.exit("[~] No images detected on the page.")


def main():
    html = get_source("https://w3.ibm.com/bluepages/profile.html?uid=C-PSU5897")
    tags = filter_images(html)
    for tag in tags:
        src = tag.get("src")
        if src:
            (link, name) = src.groups()
            if not link.startswith("http"):
                link = "https://w3.ibm.com/bluepages/" + link
            r = requests.get(src, stream=True)
            f = open(name.split("/")[-1], "wb")
            shutil.copyfileobj(r.raw, f)


if __name__ == '__main__':
    main()
