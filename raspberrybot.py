# set encoding: utf-8
import config
import telebot
import utils


class TelegramBot(telebot.TeleBot):
    def __init__(self, token, threaded=True):
        super(TelegramBot, self).__init__(token, threaded)
        self._user_id = self.read_user_id()
        if self._user_id:
            print("Listening user %d" % self.user_id)
            self.send_init_message()

    def send_init_message(self):
        self.send_message(self.user_id, "Raspberry Pi powered on")

    @staticmethod
    def read_user_id():
        try:
            with open(config.USER_ID_FILE, 'r') as user_id_file:
                return int(user_id_file.readline())
        except IOError:
            return None

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id
        with open(config.USER_ID_FILE, 'w') as user_id_file:
            user_id_file.write(str(self.user_id))

    def validate_user(self, message):
        return message.chat.id == self.user_id


bot = TelegramBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not bot.user_id:
        bot.user_id = message.chat.id
        bot.reply_to(message, "Added user %d" % bot.user_id)
    elif message.chat.id == bot.user_id:
        bot.reply_to(message, "Welcome back!")
    else:
        bot.reply_to(message, "Invalid user. The Bot is linked with other user %s" % bot.user_id)


@bot.message_handler(commands=['public_ip'], func=bot.validate_user)
def get_public_ip(message):
    bot.reply_to(message, utils.get_public_ip())


@bot.message_handler(commands=['local_ip'], func=bot.validate_user)
def get_local_ip(message):
    bot.reply_to(message, utils.get_local_ip())


@bot.message_handler(commands=['torrent_add'], func=bot.validate_user)
def torrent_management(message):
    args = message.text.split()
    if len(args) < 2:
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
def torrent_management(message):
    response = utils.torrent_list()
    bot.reply_to(message, response)


@bot.message_handler(func=bot.validate_user)
def invalid_command(message):
    bot.reply_to(message, "Invalid command '%s'" % message.text)


@bot.message_handler(func=lambda m: True)
def unauthorized_user(message):
    bot.reply_to(message, "User not allowed")


if __name__ == "__main__":
    bot.polling()
