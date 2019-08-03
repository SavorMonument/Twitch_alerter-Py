#!/usr/bin/env python3

from gi.repository import Gio

import os
import gi
import time

import twitch_api

ICON_PATH = os.path.expanduser("~") + "/.icons/"

class NotificationService():

    def __init__(self, name):
        gi.require_version('Gio', '2.0')
        self.__app = Gio.Application.new(name, Gio.ApplicationFlags.FLAGS_NONE)
        self.__app.register()

    def send_notification(self, title, body, icon_path):
        notification = Gio.Notification.new(title)
        notification.set_body(body)
        # notification.set_default_action("app.printS")
        self.__set_notif_icon(notification, icon_path)
        self.__app.send_notification(None, notification)

    def __set_notif_icon(self, notification, path):
        notification.set_icon(Gio.FileIcon.new(
            Gio.File.new_for_path(path)))


class StreamStatus():

    def __init__(self):

        self.__ONLINE = True
        self.__OFFLINE = False

        self.streamer_status = {}
        self.__callback_list_active_to_inactive = []
        self.__callback_list_inactive_to_active = []

    '''
    Call this function to update the stream status
    All the streams from the active_streams list are considered
    live and the ones not present are considered offline
    '''
    def update_active_streames(self, active_streames: list):

        for name, status in self.streamer_status.items():
            new_status = name in active_streames
            if status == self.__ONLINE and new_status == self.__OFFLINE:
                self.streamer_status[name] = self.__OFFLINE
                self.__call_active_to_inactive(name)

        for active_stream in active_streames:
            if self.streamer_status.get(active_stream, self.__OFFLINE)\
                    == self.__OFFLINE or active_stream not in self.streamer_status:

                self.streamer_status[active_stream] = self.__ONLINE
                self.__call_inactive_to_active(active_stream)

    def add_active_to_inactive_callback(self, callback):
        self.__callback_list_active_to_inactive.append(callback)

    def add_inactive_to_active_callback(self, callback):
        self.__callback_list_inactive_to_active.append(callback)

    def __call_active_to_inactive(self, name):
        for callback in self.__callback_list_active_to_inactive:
            callback(name)

    def __call_inactive_to_active(self, name):
        for callback in self.__callback_list_inactive_to_active:
            callback(name)


def download_user_icons(user_ID, users: list):
    user_data_by_username = twitch_api.UserDataByUsername(user_ID)
    user_data = user_data_by_username.get_data(users)
    user_data_parser = twitch_api.UserDataParser(user_data)
    for user in users:
        user_icon = twitch_api.UserIcon(user,
                                        user_data_parser.get_user_icon_URL(user))
        user_icon.download_icon_to_path(ICON_PATH)


def terminal_print_online(name):
    print("{1} - {0} went live."
          .format(name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def terminal_print_offline(name):
    print("{1} - {0} went offline."
          .format(name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
