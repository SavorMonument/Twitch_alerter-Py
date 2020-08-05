
from app import StreamStatus

from unittest.mock import patch
from unittest.mock import MagicMock

import unittest


class TestStreamStatus(unittest.TestCase):

    def setUp(self):
        self.stream_status = StreamStatus()
        self.test_list_streams = ["kit", "test1"]

    def test_after_one_update__all_are_True(self):

        self.stream_status.update_active_streames(self.test_list_streams)

        self.assertEqual({name: True for name in self.test_list_streams},
                         self.stream_status.streamer_status)

    def test_after_two_updates__all_are_still_True(self):

        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames(self.test_list_streams)

        self.assertEqual({name: True for name in self.test_list_streams},
                         self.stream_status.streamer_status)

    def test_after_two_different_updates__the_common_are_True(self):

        test_list_streams2 = ["test2", "test3"]
        expected = {name: True for name in test_list_streams2}
        expected.update({name: False for name in self.test_list_streams})

        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames(test_list_streams2)

        self.assertEqual(expected, self.stream_status.streamer_status)

    def test_after_two_different_updates__the_common_are_True2(self):

        test_list_streams2 = ["kit", "test3"]
        expected = {"kit": True, "test3": True, "test1": False}

        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames(test_list_streams2)

        self.assertEqual(expected, self.stream_status.streamer_status)

    def test_after_update_with_empty_list__all_are_False(self):

        expected = {name: True for name in self.test_list_streams}

        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames([])
        self.stream_status.update_active_streames(self.test_list_streams)

        self.assertEqual(expected, self.stream_status.streamer_status)

    def test_after_update_with_one_elem__that_elem_is_True(self):

        expected = {name: True for name in self.test_list_streams}
        expected.update({"test2": True})

        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames([])
        self.test_list_streams.append("test2")
        self.stream_status.update_active_streames(self.test_list_streams)

        self.assertEqual(expected, self.stream_status.streamer_status)

    def test_after_online_update__the_inactive_to_active_is_called(self):

        self.test_list_streams = ["kit"]
        call = MagicMock()

        self.stream_status.add_inactive_to_active_callback(call)
        self.stream_status.update_active_streames(self.test_list_streams)

        call.assert_called_with("kit")

    def test_after_offline_update__the_active_to_inactive_is_called(self):

        self.test_list_streams = ["kit"]
        call = MagicMock()

        self.stream_status.add_active_to_inactive_callback(call)
        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.update_active_streames([])

        call.assert_called_with("kit")

    def test_after_online_update__the_active_to_inactive_is_not_called(self):

        self.test_list_streams = ["kit"]
        call = MagicMock()

        self.stream_status.add_active_to_inactive_callback(call)
        self.stream_status.update_active_streames(self.test_list_streams)

        assert not call.called

    def test_after_offline_update__the_inactive_to_active_is_not_called(self):

        self.test_list_streams = ["kit"]
        call = MagicMock()

        self.stream_status.update_active_streames(self.test_list_streams)
        self.stream_status.add_inactive_to_active_callback(call)
        self.stream_status.update_active_streames([])

        assert not call.called

unittest.main()
# class TestArgsResolver(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def test_(self):
#         pass
