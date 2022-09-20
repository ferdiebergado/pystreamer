#!/usr/bin/env python3

import mpv
import dbus
import json
import os
import time

DURATION = 60 * 30  # 30 minutes
APP_NAME = "streamer.py"
ICON_FILE = "./Guyman-Helmet-Music-icon.png"
DATA_FILE = "./stations.json"
TIMEOUT = 5000  # 5 seconds


def notify(summary, body):
    item = "org.freedesktop.Notifications"

    dbus_interface = dbus.Interface(
        dbus.SessionBus().get_object(item, "/" + item.replace(".", "/")), item
    )

    dbus_interface.Notify(
        APP_NAME,
        0,
        os.path.abspath(ICON_FILE),
        summary,
        body,
        [],
        {"urgency": 1},
        TIMEOUT,
    )


def main():
    with open(DATA_FILE) as station_file:

        stations = json.load(station_file)

    player = mpv.MPV(
        ytdl=True,
        input_default_bindings=True,
        input_vo_keyboard=True,
        terminal=True,
        input_terminal=True,
    )

    @player.property_observer("metadata")
    def metadata_observer(_name, value):

        if value:
            title = value.get("icy-title")

            if title:
                name = value["icy-name"]

                notify("Now Playing", f"{title}\n{name}")

                print(f"\x1b]2;{title}\x07")

    for station in stations:
        player.playlist_append(station["url"])

    while True:

        print("\nTuning in...\n")

        player.playlist_shuffle()
        player.playlist_pos = 0
        player.wait_until_playing()

        time.sleep(DURATION)


if __name__ == "__main__":
    main()
