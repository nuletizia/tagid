import os
import copy
import time
import json
import base64
import requests
from time import sleep
from io import BytesIO
from PIL import Image, ImageFile, ImageFilter, ImageCms


## -----------READ/WRITE FUNCTIONS------------
def open_image_from_url(url):
    response = requests.get(url, stream=True)
    if not response.ok:
        print(response)

    image = Image.open(BytesIO(response.content))
    return image

def open_image_from_path(path):
    f = open(path, 'rb')
    buffer = BytesIO(f.read())
    image = Image.open(buffer)
    return image

    return BytesIO(response.content)

def im_2_B(image):
    # Convert Image to buffer
    buff = BytesIO()

    if image.mode == 'CMYK':
        image = ImageCms.profileToProfile(image, 'ISOcoated_v2_eci.icc', 'sRGB Color Space Profile.icm', renderingIntent=0, outputMode='RGB')

    image.save(buff, format='PNG',icc_profile=image.info.get('icc_profile'))
    img_str = buff.getvalue()
    return img_str

def im_2_buffer(image):
    # Convert Image to bytes 
    buff = BytesIO()

    if image.mode == 'CMYK':
        image = ImageCms.profileToProfile(image, 'ISOcoated_v2_eci.icc', 'sRGB Color Space Profile.icm', renderingIntent=0, outputMode='RGB')

    image.save(buff, format='PNG',icc_profile=image.info.get('icc_profile'))
    return buff

def b64_2_img(data):
    # Convert Base64 to Image
    buff = BytesIO(base64.b64decode(data))
    return Image.open(buff)
    
def im_2_b64(image):
    # Convert Image 
    buff = BytesIO()
    image.save(buff, format='PNG')
    img_str = base64.b64encode(buff.getvalue()).decode('utf-8')
    return img_str


## -----------PROCESSING FUNCTIONS------------
def start_call(email, password):
    # Get token

    URL_API = 'https://api.piktid.com/api'
    print(f'Logging to: {URL_API}')

    response = requests.post(URL_API+'/tokens', data={}, auth=(email, password))
    response_json = json.loads(response.text)
    ACCESS_TOKEN = response_json['access_token']
    REFRESH_TOKEN = response_json['refresh_token']

    return {'access_token':ACCESS_TOKEN, 'refresh_token':REFRESH_TOKEN, 'url_api':URL_API}


def refresh_call(TOKEN_DICTIONARY):
    # Get token using only access and refresh tokens, no mail and psw
    URL_API = TOKEN_DICTIONARY.get('url_api')
    response = requests.put(URL_API+'/tokens', json=TOKEN_DICTIONARY)
    response_json = json.loads(response.text)
    ACCESS_TOKEN = response_json['access_token']
    REFRESH_TOKEN = response_json['refresh_token']

    return {'access_token':ACCESS_TOKEN, 'refresh_token':REFRESH_TOKEN, 'url_api':URL_API}

# UPLOAD
def get_tags_call(img, TOKEN_DICTIONARY):
    TOKEN = TOKEN_DICTIONARY.get('access_token','')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.post(URL_API+'/getTags',
                            headers={'Authorization': 'Bearer '+TOKEN},
                            json={'base64':im_2_b64(img)},
                            )

    if response.status_code == 401:
        TOKEN_DICTIONARY = refresh_call(TOKEN_DICTIONARY)
        TOKEN = TOKEN_DICTIONARY.get('access_token','')
        # try with new TOKEN
        response = requests.post(URL_API+'/getTags', 
            headers={'Authorization': 'Bearer '+TOKEN},
            json={'base64':im_2_b64(img)}
        )

    response_json = json.loads(response.text)    
    return response_json



def get_caption_call(img, TOKEN_DICTIONARY):
    TOKEN = TOKEN_DICTIONARY.get('access_token','')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.post(URL_API+'/getCaption',
                            headers={'Authorization': 'Bearer '+TOKEN},
                            json={'base64':im_2_b64(img)},
                            )

    if response.status_code == 401:
        TOKEN_DICTIONARY = refresh_call(TOKEN_DICTIONARY)
        TOKEN = TOKEN_DICTIONARY.get('access_token','')
        # try with new TOKEN
        response = requests.post(URL_API+'/getCaption', 
            headers={'Authorization': 'Bearer '+TOKEN},
            json={'base64':im_2_b64(img)}
        )
    
    response_json = json.loads(response.text)
    return response_json.get('data')
    
    
def get_answer_call(img, question, TOKEN_DICTIONARY):
    TOKEN = TOKEN_DICTIONARY.get('access_token','')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.post(URL_API+'/getCaption',
                            headers={'Authorization': 'Bearer '+TOKEN},
                            json={'base64':im_2_b64(img), "question":question},
                            )

    if response.status_code == 401:
        TOKEN_DICTIONARY = refresh_call(TOKEN_DICTIONARY)
        TOKEN = TOKEN_DICTIONARY.get('access_token','')
        # try with new TOKEN
        response = requests.post(URL_API+'/getCaption', 
            headers={'Authorization': 'Bearer '+TOKEN},
            json={'base64':im_2_b64(img), "question":question}
        )

    response_json = json.loads(response.text)
    
    return response_json.get('data')