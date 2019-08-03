
from app import StreamStatus

from unittest.mock import patch
from unittest.mock import MagicMock

import unittest


class TestStreamStatus(unittest.TestCase):

    def setUp(self):
        self.stream_status = StreamStatus()
        self.test_list_streams = ["kit", "test1"]

    def test_update_active_streames_one_update(self):

        self.stream_status.update_active_streames(self.test_list_streams)

        self.assertEqual({name: True for name in self.test_list_streams},
                         self.stream_status.streamer_status)

    def test_update_active_streames_two_updates_same_streames(self):

        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames(self.test_list_streams)

        self.assertEqual({name: True for name in self.test_list_streams},
                         self.stream_status.streamer_status)

    def test_update_active_streames_two_updates_different_streames(self):

        test_list_streams2 = ["test2", "test3"]
        expected = {name: True for name in test_list_streams2}
        expected.update({name: False for name in self.test_list_streams})

        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames(test_list_streams2)

        self.assertEqual(expected, self.stream_status.streamer_status)

    def test_update_active_streames_two_updates_different_streames2(self):

        test_list_streams2 = ["kit", "test3"]
        expected = {"kit": True, "test3": True, "test1": False}

        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames(test_list_streams2)

        self.assertEqual(expected, self.stream_status.streamer_status)

    def test_update_active_streames_live_offline_live(self):

        expected = {name: True for name in self.test_list_streams}

        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames([])
        self.stream_status.update_active_streames(self.test_list_streams)

        self.assertEqual(expected, self.stream_status.streamer_status)

    def test_update_active_streames_live_offline_live2(self):

        expected = {name: True for name in self.test_list_streams}
        expected.update({"test2": True})

        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames([])
        self.test_list_streams.append("test2")
        self.stream_status.update_active_streames(self.test_list_streams)

        self.assertEqual(expected, self.stream_status.streamer_status)

    def test_inactive_to_active_callback(self):

        self.test_list_streams = ["kit"]
        call = MagicMock()

        self.stream_status.add_inactive_to_active_callback(call)
        self.stream_status.update_active_streames(self.test_list_streams)

        call.assert_called_with("kit")

    def test_active_to_inactive_callback(self):

        self.test_list_streams = ["kit"]
        call = MagicMock()

        self.stream_status.add_active_to_inactive_callback(call)
        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames([])

        call.assert_called_with("kit")


unittest.main()
