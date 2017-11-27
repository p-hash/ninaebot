#!/usr/bin/env python3
import hy
import ltsm

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import telebot
import os 

token = os.environ.get('TOKEN')
if not token:
  print('Specify TOKEN environment variable')
  exit(1)
tgapi = telebot.TeleBot(token)

chatterbot = ChatBot("Ninaebot")
chatterbot.set_trainer(ChatterBotCorpusTrainer)
chatterbot.train("./data/")


@tgapi.message_handler(func=lambda message: True)
def echo_all(message):
  if message.text:
    tgapi.reply_to(message, chatterbot.get_response(message.text))

tgapi.polling()

