import unittest

from raspberrybot import utils
from raspberrybot.models import Torrent

TRANSMISSION_MSG_SUCCESS = 'localhost:9091/transmission/rpc/ responded: "success"'
TRANSMISSION_MSG_ADD_INVALID_TORRENT = "Error: invalid or corrupt torrent file"
TORRENT_MAGNET = "magnet:?xt=urn:btih:20130AA512BE804B52C6D751DFA7070E308037CE&dn=the+martian+2015+hdrip+xvid+etrg&tr=udp%3A%2F%2Ftracker.publicbt.com%2Fannounce&tr=udp%3A%2F%2Fglotorrents.pw%3A6969%2Fannounce"


class TestUtils(unittest.TestCase):
    ip_regex = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"

    def test_get_local_ip(self):
        self.assertRegex(utils.get_local_ip(), self.ip_regex)

    def test_get_public_ip(self):
        self.assertRegex(utils.get_public_ip(), self.ip_regex)

    def test_get_uptime(self):
        self.assertIn("days", utils.get_uptime())

    def test_torrent_add_empty(self):
        self.assertEqual(utils.torrent_add(""),
                         TRANSMISSION_MSG_ADD_INVALID_TORRENT)

    def test_torrent_add_invalid(self):
        self.assertEqual(utils.torrent_add("magnet:?xt=urn:btih:2013fdfff"),
                         TRANSMISSION_MSG_ADD_INVALID_TORRENT)

    def test_torrent_remove_invalid(self):
        self.assertEqual(utils.torrent_remove(-1), TRANSMISSION_MSG_SUCCESS)

    def test_torrent_list(self):
        torrents = utils.torrent_list()
        self.assertIsInstance(torrents[0], Torrent)

    def test_add_list_info_and_remove(self):
        count_before = len(utils.torrent_list())
        self.assertEqual(utils.torrent_add(TORRENT_MAGNET), TRANSMISSION_MSG_SUCCESS)
        self.assertEqual(utils.torrent_add(TORRENT_MAGNET), 'Error: duplicate torrent')
        torrents = utils.torrent_list()
        count_after = len(torrents)
        added_torrent = torrents[-1]
        self.assertTrue(utils.torrent_info(added_torrent.id))
        self.assertEqual(count_after, count_before + 1)
        self.assertEqual(utils.torrent_remove(added_torrent.id), TRANSMISSION_MSG_SUCCESS)


if __name__ == '__main__':
    unittest.main()
