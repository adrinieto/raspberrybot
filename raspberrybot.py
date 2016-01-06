# set encoding: utf-8
import json
import logging
import logging.config

import config
import telebot
import utils

with open(config.LOGGING_CONFIG_FILE) as config_file:
    logging.config.dictConfig(json.load(config_file))

log = logging.getLogger(__name__)


class TelegramBot(telebot.TeleBot):
    def __init__(self, token, threaded=True):
        super(TelegramBot, self).__init__(token, threaded)
        log.info("Starting bot...")
        self._user_id = self.read_user_id()
        if self._user_id:
            log.info("Listening to user %d" % self.user_id)
            self.send_init_message()

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
        log.info("Seting user_id to " % self.user_id)
        self._user_id = user_id
        with open(config.USER_ID_FILE, 'w') as user_id_file:
            log.info("Writing user_id to file '%s'" % config.USER_ID_FILE)
            user_id_file.write(str(self.user_id))

    def validate_user(self, message):
        return message.chat.id == self.user_id


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
    bot.reply_to(message, response)
    # if response:
    #     bot.reply_to(message, "Torrent '%s' added" % response)
    # else:
    #     bot.reply_to(message, "An error happened adding the torrent")


@bot.message_handler(commands=['torrent_list'], func=bot.validate_user)
def torrent_list(message):
    log.info("Handling command list torrents - %s" % message.text)
    response = utils.torrent_list()
    bot.reply_to(message, response)


@bot.message_handler(func=bot.validate_user)
def invalid_command(message):
    log.warn("Invalid command - %s " % message.text)
    bot.reply_to(message, "Invalid command '%s'" % message.text)


@bot.message_handler(func=lambda m: True)
def unauthorized_user(message):
    log.warn("Unauthorized user - %s:%s " % (message.chat.id, message.text))
    bot.reply_to(message, "User not allowed")


if __name__ == "__main__":
    bot.polling()
