#!/usr/bin/env python3

import app
import twitch_api

import json
import os
import sys
import time

if len(sys.argv) < 3:
    print("Usage: [Twitch_user_ID] [Stramer_names...]")
    exit(0)

client_ID = sys.argv[1]
selected_streamers = sys.argv[2:]

notif_service = app.NotificationService("notif.service")
app.download_user_icons(client_ID, selected_streamers)


def send_notification(name):
    notif_service.send_notification(
        name + " is live", "Go to twitch.tv to watch",
        app.ICON_PATH + "{}.png".format(name.lower()))


streamer_status = app.StreamStatus()
# You can add any functionality for when a stream changes state here
# For example you can make a function and add a callback to
# streamer_status.add_active_to_inactive_callback() and it will call it
# when the state changes
# -------
streamer_status.add_inactive_to_active_callback(send_notification)
streamer_status.add_inactive_to_active_callback(app.terminal_print_online)
streamer_status.add_active_to_inactive_callback(app.terminal_print_offline)
# -------


stream_data_by_username = twitch_api.StreamDataByUsername(client_ID)
while True:
    user_data = stream_data_by_username.get_data(selected_streamers)
    # print(json.dumps(json.loads(user_data), indent=4, sort_keys=True))
    active_streames = twitch_api.StreamDataParser(user_data)\
        .get_list_of_active_streams()
    streamer_status.update_active_streames(active_streames)

    time.sleep(15)
