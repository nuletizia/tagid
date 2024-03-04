<p align="center">
  <img src="https://studio.piktid.com/logo.svg" alt="TagID by PiktID logo" width="150">
  </br>
  <h3 align="center"><a href="[https://studio.piktid.com](https://studio.piktid.com)">TagID by PiktID</a></h3>
</p>


# TagID
[![Official Website](https://img.shields.io/badge/Official%20Website-piktid.com-blue?style=flat&logo=world&logoColor=white)](https://piktid.com)
[![Discord Follow](https://dcbadge.vercel.app/api/server/FJU39e9Z4P?style=flat)](https://discord.com/invite/FJU39e9Z4P)

TagID is a GenAI tagging tool which produces accurate textual descriptions of images. 


## About
TagID utilizes generative models to intelligently describe and annotate images. It can be extremely powerful in the following scenarios:

- <ins>Image keywording</ins>: It provides quick and accurate keywords to facilitate storing of your images.
- <ins>Image captioning</ins>: It provides precise short and long captions which can be use to help users understand what is the message of the image. 

## Getting Started
<a target="_blank" href="https://colab.research.google.com/drive/1D0yFV_xwSsWwmYHBJP07g2IlSDiZXbLv?usp=sharing">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

The following instructions suppose you have already installed a recent version of Python. For a general overview, please visit the <a href="https://api.piktid.com/docs">API documentation</a>.
To use any PiktID API, an access token is required. 

> **Step 0** - Register <a href="https://studio.piktid.com">here</a>. 10 credits are given for free to all new users.

> **Step 1** - Clone the TagID library
```bash
# Installation commands
$ git clone https://github.com/piktid/tagid.git
$ cd tagid
$ pip install -r requirements.txt
```

> **Step 2** - Export the email and password as environmental variables
```bash
$ export TAGID_EMAIL={Your email here}
$ export TAGID_PASSWORD={Your password here}
```

> **Step 3** - Change in main.py the URL of the image to be described or pass it as argument
```python
...
url = 'your-url'
...
```

> **Step 4** - Run the main function
```bash
$ python3 main.py --url 'your-url'
```

You can also pass the path to the local file
```bash
$ python3 main.py --filepath 'your/path/to/the/file'
```

Without any additional argument, TagID provides keywords and captions. However, you can also ask questions about the image as in the following: 
```bash
$ python3 main.py --question 'What is the subject of the image?'
```

## Contact
office@piktid.com
