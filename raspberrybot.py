# set encoding: utf-8
import config
import telebot
import utils


class TelegramBot(telebot.TeleBot):
    def __init__(self, token, threaded=True):
        super(TelegramBot, self).__init__(token, threaded)
        self._user_id = self.read_user_id()

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
        bot.reply_to(message, "Añadido usuario %d" % bot.user_id)
    elif message.chat.id == bot.user_id:
        bot.reply_to(message, "Welcome back!")
    else:
        bot.reply_to(message, "Ya existe un usuario registrado '%d'" % bot.user_id)


@bot.message_handler(commands=['public_ip'], func=bot.validate_user)
def get_public_ip(message):
    bot.reply_to(message, utils.get_public_ip())


@bot.message_handler(commands=['local_ip'], func=bot.validate_user)
def get_local_ip(message):
    bot.reply_to(message, utils.get_local_ip())


@bot.message_handler(func=bot.validate_user)
def invalid_command(message):
    bot.reply_to(message, "Comando inválido")


@bot.message_handler(func=lambda m: True)
def unauthorized_user(message):
    bot.reply_to(message, "Usuario incorrecto")


if __name__ == "__main__":
    print("Listening user %d" % bot.user_id)
    bot.polling()
