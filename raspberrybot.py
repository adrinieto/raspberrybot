import json
import logging.config
import threading

from collections import defaultdict

import telebot
from raspberrybot import config, utils
from raspberrybot.models import TorrentStatus

INTERVAL = 60
EMOJI_THUMBS_UP = "\U0001F44D"

with open(config.LOGGING_CONFIG_FILE) as config_file:
    logging.config.dictConfig(json.load(config_file))

log = logging.getLogger(__name__)


class TelegramBot(telebot.TeleBot):
    def __init__(self, token, threaded=True):
        super(TelegramBot, self).__init__(token, threaded)
        log.info("Starting bot...")
        self.downloading_torrents = set()
        self._user_id = self.read_user_id()
        if self._user_id:
            log.info("Listening to user %d" % self.user_id)
            self.send_init_message()
            self.check_if_downloaded()

    def send_init_message(self):
        log.info("Sending init message")
        self.send_message(self.user_id, "Raspberry Pi powered on")

    @staticmethod
    def read_user_id():
        try:
            with open(config.USER_ID_FILE, 'r') as user_id_file:
                log.info("Reading user_id from file '%s'" % config.USER_ID_FILE)
                return int(user_id_file.readline())
        except IOError as e:
            log.warn("Read user fail: %s" % e)
            return None

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        log.info("Setting user_id to %s" % user_id)
        self._user_id = user_id
        with open(config.USER_ID_FILE, 'w') as user_id_file:
            log.info("Writing user_id to file '%s'" % config.USER_ID_FILE)
            user_id_file.write(str(self.user_id))

    def validate_user(self, message):
        return message.chat.id == self.user_id

    def check_if_downloaded(self):
        torrents = utils.torrent_list()
        torrents_by_status = defaultdict(set)
        for t in torrents:
            if t.done == "100%":
                torrents_by_status["done"].add(t)
            else:
                torrents_by_status["downloading"].add(t)

        recently_completed = (self.downloading_torrents - torrents_by_status["downloading"]) & torrents_by_status["done"]
        self.downloading_torrents = torrents_by_status["downloading"]
        for t in recently_completed:
            self.send_message(self._user_id, "Torrent '_%s_' has been downloaded " % t.name + EMOJI_THUMBS_UP, parse_mode="Markdown")
        threading.Timer(INTERVAL, self.check_if_downloaded).start()


bot = TelegramBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    log.info("Handling command start")
    if not bot.user_id:
        log.info("New user")
        bot.user_id = message.chat.id
        bot.reply_to(message, "Added user %d" % bot.user_id)
    elif message.chat.id == bot.user_id:
        log.info("Previous user")
        bot.reply_to(message, "Welcome back!")
    else:
        log.info("Invalid user %d" % message.chat.id)
        bot.reply_to(message, "Invalid user. The Bot is linked with other user %s" % bot.user_id)


@bot.message_handler(commands=['public_ip'], func=bot.validate_user)
def get_public_ip(message):
    log.info("Handling command get public ip - %s" % message.text)
    bot.reply_to(message, utils.get_public_ip())


@bot.message_handler(commands=['local_ip'], func=bot.validate_user)
def get_local_ip(message):
    log.info("Handling command get local ip - %s" % message.text)
    bot.reply_to(message, utils.get_local_ip())


@bot.message_handler(commands=['uptime'], func=bot.validate_user)
def get_uptime(message):
    log.info("Handling command uptime - %s" % message.text)
    bot.reply_to(message, utils.get_uptime())


@bot.message_handler(commands=['torrent_add'], func=bot.validate_user)
def torrent_add(message):
    log.info("Handling command add torrent - %s" % message.text)
    args = message.text.split()
    if len(args) < 2:
        log.warn("Missing torrent URL")
        bot.reply_to(message, "Missing torrent URL. Usage: /torrent_add [URL]")
        return
    url = args[1]
    response = utils.torrent_add(url)
    if "success" in response:
        log.info("Torrent added")
        bot.reply_to(message, "Torrent added")
    else:
        log.info("Error adding torrent")
        bot.reply_to(message, response)


@bot.message_handler(commands=['torrent_list'], func=bot.validate_user)
def torrent_list_by_status(message):
    log.info("Handling command list torrents - %s" % message.text)
    torrents = utils.torrent_list()
    log.info("Torrents: %s", torrents)

    torrents_by_type = defaultdict(list)

    for torrent in torrents:
        torrents_by_type[torrent.status].append(torrent)

    response = ""
    for key in torrents_by_type.keys():
        response += "*%s*\n" % TorrentStatus.conversion_to_string[key]
        for t in torrents_by_type[key]:
            response += t.format_telegram() + "\n"

    bot.reply_to(message, response, parse_mode="Markdown")


@bot.message_handler(commands=['torrent_info'], func=bot.validate_user)
def torrent_info(message):
    log.info("Handling command info torrent - %s" % message.text)
    args = message.text.split()
    if len(args) < 2:
        log.warn("Missing torrent ID")
        bot.reply_to(message, "Missing torrent ID. Usage: /torren_info [TORRENT_ID]")
        return
    torrent_id = args[1]
    bot.reply_to(message, utils.torrent_info(torrent_id))


@bot.message_handler(commands=['torrent_remove'], func=bot.validate_user)
def torrent_remove(message):
    log.info("Handling command remove torrent - %s" % message.text)
    args = message.text.split()
    if len(args) < 2:
        log.warn("Missing torrent ID")
        bot.reply_to(message, "Missing torrent ID. Usage: /torrent_remove [TORRENT_ID]")
        return
    torrent_id = args[1]
    bot.reply_to(message, utils.torrent_remove(torrent_id))


@bot.message_handler(func=bot.validate_user)
def invalid_command(message):
    log.warn("Invalid command - %s " % message.text)
    bot.reply_to(message, "Invalid command '%s'" % message.text)


@bot.message_handler(func=lambda m: True)
def unauthorized_user(message):
    log.warn("Unauthorized user - %s:%s " % (message.chat.id, message.text))
    bot.reply_to(message, "User not allowed")


def polling():
    # try:
    bot.polling(none_stop=True)
    # except Exception:
    #     log.exception("Error during polling. Waiting to reconnect...")
    #     time.sleep(5 * 60)
    #     polling()


if __name__ == "__main__":
    polling()
