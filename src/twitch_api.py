#!/usr/bin/env python3

from PIL import Image

import requests
import json


class StreamData():

    def get_data(self, users: list):
        response = requests\
            .get(self._base_url, headers={"Client-ID": self._client_ID},
                 params={self._parameter_name: [user for user in users]})
        if not response.ok:
            raise Exception("Server response error with status code: "
                            + response.status_codes)
        return response.content.decode("UTF-8")


class StreamDataByUsername(StreamData):

    def __init__(self, client_ID: str):
        self._base_url = "https://api.twitch.tv/helix/streams"
        self._parameter_name = "user_login"
        self._client_ID = client_ID


class UserDataByUsername(StreamData):

    def __init__(self, client_ID: str):
        self._base_url = "https://api.twitch.tv/helix/users"
        self._parameter_name = "login"
        self._client_ID = client_ID


class UserFollowsData_v5():

    """
    This uses the depricated v5 api, the new one does not have this
    functionality
    user_ID - the user which you are targeting
    client_ID - twitch api client_ID
    """

    def __init__(self, client_ID: str):
        self._base_url =\
            "https://api.twitch.tv/kraken/users/<user ID>/follows/channels"
        self._client_ID = client_ID

    def get_data(self, user_ID: str):
        response = requests\
            .get(self._base_url.replace("<user ID>", user_ID),
                 headers={"Client-ID": self._client_ID,
                          "Accept": "application/vnd.twitchtv.v5+json"})
        if not response.ok:
            raise Exception(
                "Server response error with status code: {}\n URL: {}"
                .format(str(response.status_code), response.url ) )
        return response.content.decode("UTF-8")


class StreamDataParser():

    def __init__(self, stream_data: dict):
        self.__stream_data = json.loads(stream_data).get("data")

    def get_list_of_active_streams(self):
        active_streamers = []
        for stream in self.__stream_data:
            active_streamers.append(stream["user_name"])

        return active_streamers


class UserDataParser():

    '''This takes a json as a string, supports multiple users per json'''

    def __init__(self, data):
        self.__user_data = json.loads(data).get("data")

    def get_user_icon_URL(self, username):
        for user_data in self.__user_data:
            if (user_data["login"] == username.lower()):
                return user_data["profile_image_url"]

    def get_user_id(self, username):
        for user_data in self.__user_data:
            if (user_data["login"] == username.lower()):
                return user_data["id"]


class UserIcon():

    def __init__(self, username, icon_url):
        self.__icon_url = icon_url
        self.__username = username

    def download_icon_to_path(self, path):
        response = requests.get(self.__icon_url, stream=True)
        response.raw.decode_content = True
        image = Image.open(response.raw)
        image.save(path + self.__username + ".png", "PNG")
