#!/usr/bin/env python3

import urllib
import twitch_api
import requests
from PIL import Image

user_ID = "0pf437y3pf6mi69dxyn14699fpo182"
user = "kitboga"

user_data_by_username = twitch_api.UserDataByUsername(user_ID)
user_data = user_data_by_username.get_user_data([user])
user_data_parser = twitch_api.UserDataParser(user_data)

url = user_data_parser.getUserIconURL(user)

response = requests.get(url, stream=True)
response.raw.decode_content = True
image = Image.open(response.raw)

image.save("/home/goia/.icons/" + user + ".png", "PNG")
