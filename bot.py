from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import telebot
import os 

tgapi = telebot.TeleBot(os.environ['TOKEN'])

chatterbot = ChatBot("Ninaebot")
chatterbot.set_trainer(ChatterBotCorpusTrainer)
chatterbot.train("./data/")


@tgapi.message_handler(func=lambda message: True)
def echo_all(message):
  if message.text:
    tgapi.reply_to(message, chatterbot.get_response(message.text))

tgapi.polling()

