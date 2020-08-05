#!/usr/bin/env python3

from PIL import Image

import requests
import json
import time

class TwitchApiV5():

    OAUTH_URL = 'https://id.twitch.tv/oauth2/token'

    def __init__(self, client_ID, client_secret):
        self._client_ID = client_ID
        self._client_secret = client_secret
        self.token_expire_time = 0
        self.token = ''

    def get_with_token(self, url, params):
        if self._is_token_expired():
            self._refresh_token()
        headers = {"Client-ID": self._client_ID, 'Authorization': 'Bearer %s' % self.token}
        return self._get(url, params, headers)

    def _refresh_token(self):
        params = {'client_id': self._client_ID,\
                'client_secret': self._client_secret,\
                'grant_type': 'client_credentials'}

        r = self._post(self.OAUTH_URL, params)
        token_info = json.loads(r)

        self.token_expire_time = time.time() + token_info['expires_in']
        self.token = token_info['access_token']

    def _is_token_expired(self):
        return time.time() > self.token_expire_time

    def _get(self, url, params, headers={}):
        response = requests.get(url, params=params, headers=headers)
        # print('Rate remaining: %s' % response.headers['Ratelimit-Remaining'])
        if not response.ok:
            raise Exception("Server response error with status code: %d"\
                            % response.status_code)
        return response.content

    def _post(self, url, params, headers={}):
        response = requests.post(url, params=params, headers=headers)
        if not response.ok:
            raise Exception("Server response error with status code: %d"\
                            % response.status_code)
        return response.content

class StreamData():

    def __init__(self, client_ID, client_secret):
        self.twitch_apiv5 = TwitchApiV5(client_ID, client_secret)

    def get_data(self, users: list):
        params = {self._endpoint: [user for user in users]}
        r = self.twitch_apiv5.get_with_token(self._base_url, params)
        return r

class StreamDataByUsername(StreamData):

    def __init__(self, client_ID: str, client_secret):
        super().__init__(client_ID, client_secret)
        self._base_url = "https://api.twitch.tv/helix/streams"
        self._endpoint = "user_login"


class UserDataByUsername(StreamData):

    def __init__(self, client_ID: str, client_secret):
        super().__init__(client_ID, client_secret)
        self._base_url = "https://api.twitch.tv/helix/users"
        self._endpoint = "login"

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
