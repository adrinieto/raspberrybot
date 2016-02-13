import unittest

from raspberrybot import utils
from raspberrybot.models import Torrent


class TestUtils(unittest.TestCase):
    ip_regex = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"

    def test_get_local_ip(self):
        self.assertRegex(utils.get_local_ip(), self.ip_regex)

    def test_get_public_ip(self):
        self.assertRegex(utils.get_public_ip(), self.ip_regex)

    def test_get_uptime(self):
        self.assertIn("days", utils.get_uptime())

    def test_torrent_add_empty(self):
        self.assertEqual(utils.torrent_add(""), "Error: invalid or corrupt torrent file")

    def test_torrent_add_invalid(self):
        self.assertEqual(utils.torrent_add("magnet:?xt=urn:btih:2013fdfff"),
                         "Error: invalid or corrupt torrent file")

    def test_torrent_list(self):
        torrents = utils.torrent_list()
        self.assertIsInstance(torrents[0], Torrent)

if __name__ == '__main__':
    unittest.main()
