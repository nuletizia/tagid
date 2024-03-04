import os
import sys
import json
import argparse
import requests
from io import BytesIO
from random import randint
from PIL import Image, ImageFile, ImageFilter

from tagid_api import open_image_from_path, open_image_from_url, start_call, get_tags_call, get_caption_call, get_answer_call

if __name__ == '__main__':


    parser = argparse.ArgumentParser()


    parser.add_argument('--url', help='Image file url', type=str, default='https://images.pexels.com/photos/733872/pexels-photo-733872.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')
    parser.add_argument('--filepath', help='Input image file absolute path', type=str, default=None)
    parser.add_argument('--question', help='Question to ask about the image, e.g.: What is the subject of the image?', type=str, default=None)


    args = parser.parse_args()

    # be sure to export your email and psw as environmental variables
    EMAIL = os.getenv("TAGID_EMAIL")
    PASSWORD = os.getenv("TAGID_PASSWORD")

    # Image parameters
    URL = args.url 
    INPUT_PATH = args.filepath

    if INPUT_PATH is not None:
        if os.path.exists(INPUT_PATH):
            input_image = open_image_from_path(INPUT_PATH)
            print(f'Using as input image the file located at: {INPUT_PATH}')
        else:
            print('Wrong filepath, check again')
            sys.exit()
    else:
        try:
            input_image = open_image_from_url(URL)
            print(f'Using as input image the file located at: {URL}')
        except:
            print('Wrong URL, check again')
            sys.exit()

    # log in
    TOKEN_DICTIONARY = start_call(EMAIL, PASSWORD)


    # Call the tagID APIs
    tags = get_tags_call(input_image, TOKEN_DICTIONARY)

    # Extract the keywords from the tag output
    keywords = [entry_dict['key'] for entry_dict in tags]
    print(f'Keywords: {keywords}')

    # Call the captioning API
    caption = get_caption_call(input_image, TOKEN_DICTIONARY)
    print(f'Image description: {caption}')

    # Ask a question and get the answer
    QUESTION = args.question
    if QUESTION is not None:
        answer = get_answer_call(input_image, QUESTION, TOKEN_DICTIONARY)
        print(f'Question: {QUESTION}. Answer: {answer}')
