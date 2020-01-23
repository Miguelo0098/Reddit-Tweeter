import os
import sys
from PIL import Image
import urllib.request
from urllib.request import urlopen
import requests
import re
import hashlib

# Saves a file from a url in a local path
def save_file(img_url, file_path):
    resp = requests.get(img_url, stream=True)
    if resp.status_code==200:
        # url is OK
        with open(file_path, 'wb') as image_file:
            for chunk in resp:
                image_file.write(chunk)
        image_file.close()
        return file_path

    print('[EROR] File failed to download. Status code: ', str(resp.status_code))
    return

# Gets an image from an url
def get_media(img_url):
    IMAGE_DIR = './media' # Can be changed to another path
    # If directory does not exist, creates it
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        print('[ OK ] Media folder not found, created a new one')
    # Checks if it's a reddit image
    if any(s in img_url for s in ('i.redd.it', 'i.reddituploads.com')):
        file_name = os.path.basename(urllib.parse.urlsplit(img_url).path)
        file_extension = os.path.splitext(img_url)[-1].lower()
        #checks if it does not have an extension
        if not file_extension:
            file_extension += '.jpg'
            file_name += '.jpg'
            img_url += '.jpg'
        # Download the file
        file_path = IMAGE_DIR + '/' + file_name
        print('[ OK ] Downloading file at URL ' + img_url + ' to ' +
              file_path + ', file type identified as ' + file_extension)
        image = save_file(img_url, file_path)
        return image
    print('[EROR] URL does not point to a valid image file')
    return

